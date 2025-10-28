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
                return None


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

    # Place a small fleet: ask user to place 3 ships (lengths 3,3,2) for demo
    fleet = [("Destroyer", 3), ("Cruiser", 3), ("Patrol", 2)]
    print('Place your ships on board size', p.own_board.size)
    for ship_name, length in fleet:
        placed = False
        while not placed:
            try:
                inp = input(f"Place {ship_name} (length {length}) as 'x y H/V': ")
                sx, sy, point = inp.split()
                sx = int(sx); sy = int(sy); point = point.upper()
            except Exception:
                print('Invalid input')
                continue
            ship = Ship(ship_name, length)
            if p.place_ship(ship, sx, sy, point):
                placed = True

    # connect to server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server_ip, server_port))
    # send setup
    ships = serialize_ships(p.own_board)
    send_json(sock, {'type': 'setup', 'name': p.name, 'ships': ships})
    resp = recv_json(sock)
    if not resp or resp.get('type') != 'ok':
        print('Server did not accept setup:', resp)
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
            fr = msg.get('from')
            x = msg.get('x'); y = msg.get('y'); res = msg.get('result')
            print(f"Incoming shot from {fr} at ({x},{y}) -> {res}")
        elif t == 'game_over':
            print('Game over. Winner:', msg.get('winner'))
            break
        elif t == 'error':
            print('Error from server:', msg.get('message'))

    sock.close()


if __name__ == '__main__':
    run_client()
