import socket
import json

# per-socket receive buffers to preserve any bytes after a newline
_recv_buffers = {}
from Player import Player
from Ship import Ship


def send_json(sock, obj):
    sock.sendall((json.dumps(obj) + '\n').encode())


def recv_json(sock):
    fileno = sock.fileno()
    data = _recv_buffers.pop(fileno, b'')
    while True:
        try:
            chunk = sock.recv(4096)
        except Exception:
            return None
        if not chunk:
            return None
        data += chunk
        if b'\n' in data:
            line, rest = data.split(b'\n', 1)
            if rest:
                _recv_buffers[fileno] = rest
            try:
                return json.loads(line.decode())
            except json.JSONDecodeError:
                # malformed JSON on this line — skip it and continue with any remaining bytes
                data = rest
                if not data:
                    continue
                continue


def serialize_ships(board):
    ships = []
    for si in board.ships:
        ship = si['ship']
        positions = si['positions']
        x0, y0 = positions[0]
        # deduce orientation
        if len(positions) > 1:
            x1, y1 = positions[1]
            point = 'H' if y0 == y1 else 'V'
        else:
            point = 'H'
        ships.append({'name': ship.name, 'length': ship.length, 'x': x0, 'y': y0, 'point': point})
    return ships


def run_client(server_ip='localhost', server_port=9999):
    p = Player(name='Player')

    # Simple CLI to set player name
    name = input('Your name: ').strip() or 'Player'
    p.name = name

    def place_fleet_interactive(player):
        fleet = [("Destroyer", 3), ("Cruiser", 3), ("Patrol", 2)]
        print('Place your ships on board size', player.own_board.size)
        for ship_name, length in fleet:
            placed = False
            while not placed:
                # Display boards for reference
                player.display_your_board()
                try:
                    inp = input(f"Place {ship_name} (length {length}) as 'x y H/V': ")
                    sx, sy, point = inp.split()
                    sx = int(sx); sy = int(sy); point = point.upper()
                except Exception:
                    print('Invalid input')
                    continue
                ship = Ship(ship_name, length)
                if player.place_ship(ship, sx, sy, point):
                    placed = True

    def send_setup_and_wait(sock, player):
        ships = serialize_ships(player.own_board)
        send_json(sock, {'type': 'setup', 'name': player.name, 'ships': ships})
        resp = recv_json(sock)
        if not resp or resp.get('type') != 'ok':
            print('Server did not accept setup:', resp)
            return False
        return True

    # Initial placement
    place_fleet_interactive(p)

    # connect to server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server_ip, server_port))
    # send setup
    if not send_setup_and_wait(sock, p):
        sock.close()
        return
    print('Waiting for game to start...')

    # main event loop
    while True:
        msg = recv_json(sock)
        if msg is None:
            print('Server closed connection')
            break
        t = msg.get('type')
        if t == 'start':
            print(f"Game started. You: {msg.get('you')} Opponent: {msg.get('opponent')}")
        elif t == 'your_turn':
            p.display_boards(msg.get('opponent'))
            print('Your turn')
            while True:
                try:
                    shot = input("Enter shot x y: ")
                    sx, sy = shot.split()
                    sx = int(sx); sy = int(sy)
                except Exception:
                    print('Invalid')
                    continue
                send_json(sock, {'type': 'shot', 'x': sx, 'y': sy})
                res = recv_json(sock)
                if res and res.get('type') == 'result':
                    r = res.get('result')
                    print('Result:', r)
                    p.apply_shot_result(sx, sy, r)
                    break
        elif t == 'incoming':
            opponent = msg.get('from')
            x = msg.get('x'); y = msg.get('y'); result = msg.get('result')
            print(f"Incoming shot from {opponent} at ({x},{y}) -> {result}")
        elif t == 'game_over':
            print('Game over. Winner:', msg.get('winner'))
            # do not close yet — wait for play-again flow from server
            continue
        elif t == 'play_again_request':
            # prompt user if they want to play again
            while True:
                ans = input('Play again? (y/n): ').strip().lower()
                if ans in ('y', 'n'):
                    break
            accept = ans == 'y'
            send_json(sock, {'type': 'play_again_response', 'accept': accept})
        elif t == 'play_again_result':
            accepted = msg.get('accepted')
            if not accepted:
                print('Play again declined by one or both players. Closing.')
                break
            else:
                print('Both players accepted — server will request new setup.')
        elif t == 'request_setup':
            # server asks for a new setup — prompt player again and send
            place_fleet_interactive(p)
            if not send_setup_and_wait(sock, p):
                print('Server rejected re-setup or error. Closing.')
                break
        elif t == 'error':
            print('Error from server:', msg.get('message'))

    sock.close()


if __name__ == '__main__':
    run_client()
