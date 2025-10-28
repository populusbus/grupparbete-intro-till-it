import socket
import json
import os
import time

# debug flag toggled by environment variable BATTLE_DEBUG=1
DEBUG = os.getenv('BATTLE_DEBUG', '0') != '0'

# per-socket receive buffers to preserve any bytes after a newline
# use id(sock) as key to avoid fileno reuse issues
_recv_buffers = {}
from Player import Player
from Ship import Ship


def send_json(sock, obj):
    msg = (json.dumps(obj) + '\n').encode()
    if DEBUG:
        try:
            peer = sock.getpeername()
        except Exception:
            peer = ('?', '?')
        print(f"[{time.strftime('%H:%M:%S')}] SEND to {peer}: {obj}")
    sock.sendall(msg)


def recv_json(sock):
    key = id(sock)
    data = _recv_buffers.pop(key, b'')
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
                _recv_buffers[key] = rest
            try:
                obj = json.loads(line.decode())
                if DEBUG:
                    try:
                        peer = sock.getpeername()
                    except Exception:
                        peer = ('?', '?')
                    print(f"[{time.strftime('%H:%M:%S')}] RECV from {peer}: {obj}")
                return obj
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

    # Place a small fleet: ask user to place 3 ships (lengths 3,3,2) for demo
    #fleet = [("Destroyer", 3), ("Cruiser", 3), ("Patrol", 2)]
    fleet= [("Destroyer", 1)]
    print('Place your ships on board size', p.own_board.size)
    for ship_name, length in fleet:
        placed = False
        while not placed:
            # Display boards for reference
            p.display_your_board()
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

            play_again = input("Play again? (y/n): ").strip().lower()
            while True:
                if play_again == 'y':
                    send_json(sock, {'type': 'play_again'})
                    waiting(msg)
                elif play_again == 'n':
                    send_json(sock, {'type': 'quit'})
                    exit()
                else:
                    play_again = input("Please enter 'y' or 'n': ").strip().lower()

        elif t == 'error':
            print('Error from server:', msg.get('message'))

    sock.close()
def waiting(msg):
    print("Waiting for opponent to agree to play again...")
    if msg.get('type') == 'play_again':
        print("Both players agreed to play again. Restarting game.")
        run_client()
    elif msg.get('type') == 'quit':
        print("Opponent declined to play again.")
        run_client()

if __name__ == '__main__':
    run_client()
