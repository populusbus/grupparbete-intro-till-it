import socket
import json
import os
import time

# debug flag toggled by environment variable BATTLE_DEBUG=1
DEBUG = os.getenv('BATTLE_DEBUG', '0') != '0'

# small per-socket receive buffers to preserve any bytes after a newline
# use id(sock) as key to avoid fileno reuse issues
_recv_buffers = {}
from Board import Board
from Ship import Ship
from leaderboard import leaderboard

def recv_json(sock):
    key = id(sock)
    data = _recv_buffers.pop(key, b'')
    while True:
        try:
            chunk = sock.recv(4096)
        except Exception:
            # socket error -> treat as closed
            return None
        if not chunk:
            # connection closed
            return None
        data += chunk
        # try split by newline
        if b'\n' in data:
            line, rest = data.split(b'\n', 1)
            # store rest for next call
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
                # put the rest back into the buffer and continue reading
                data = rest
                if not data:
                    # no remaining data, continue to recv more
                    continue
                # otherwise loop will attempt to parse the remaining data (or recv more if needed)
                continue


def send_json(sock, obj):
    msg = (json.dumps(obj) + '\n').encode()
    if DEBUG:
        try:
            peer = sock.getpeername()
        except Exception:
            peer = ('?', '?')
        print(f"[{time.strftime('%H:%M:%S')}] SEND to {peer}: {obj}")
    sock.sendall(msg)


def build_board_from_setup(setup):
    b = Board()
    for s in setup:
        name = s.get('name')
        length = int(s.get('length'))
        x = int(s.get('x'))
        y = int(s.get('y'))
        point = s.get('point')
        ship = Ship(name, length)
        ok = b.place_ship(ship, x, y, point)
        if not ok:
            print(f"Warning: failed to place ship from setup: {s}")
    return b


def all_sunk(board):
    for si in board.ships:
        if not si['ship'].is_sunk():
            return False
    return True

def menu():
    option = input("1. Start Server\n2. Display leaderboard\n3. Exit\nChoose an option (1, 2 or 3): ")
    if option == '1':
        run_server()
    elif option == '2':
        lb = leaderboard()
        lb.display_leaderboard()
    elif option == '3':
        print("Exiting.")
    else:
        print("Invalid option.")
        menu()

def run_server(host='0.0.0.0', port=9999):
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((host, port))
    srv.listen(5)
    print(f"Server listening on {host}:{port} - waiting for two players...")

    clients = []
    players = []

    # Accept two clients
    while len(clients) < 2:
        conn, addr = srv.accept()
        print(f"Connected: {addr}")
        # expect a setup message as first message
        setup = recv_json(conn)
        if not setup or setup.get('type') != 'setup':
            send_json(conn, {'type': 'error', 'message': 'Expected setup'})
            conn.close()
            continue
        name = setup.get('name', f'Player{len(clients)+1}')
        ships = setup.get('ships', [])
        board = build_board_from_setup(ships)
        clients.append(conn)
        players.append({'name': name, 'board': board})
        send_json(conn, {'type': 'ok', 'message': 'setup received'})
        print(f"Registered player {name}")

    print("Two players connected. Starting game.")
    game_loop(srv, clients, players)



def game_loop(srv, clients, players):
    turn = 0
    sockets = clients
    names = [p['name'] for p in players]

    # Notify players game start
    for i, sock in enumerate(sockets):
        send_json(sock, {'type': 'start', 'you': names[i], 'opponent': names[1-i]})

    # Game loop
    while True:
        current = turn % 2
        opponent = 1 - current
        cur_sock = sockets[current]
        opp_board = players[opponent]['board']

        # Tell current it's their turn
        time.sleep(0.5)
        send_json(cur_sock, {'type': 'your_turn'})

        # Receive shot
        msg = recv_json(cur_sock)
        if msg is None:
            print(f"Player {names[current]} disconnected")
            break
        if msg.get('type') != 'shot':
            send_json(cur_sock, {'type': 'error', 'message': 'Expected shot'})
            continue
        x = int(msg.get('x'))
        y = int(msg.get('y'))
        print(f"{names[current]} -> shot at ({x},{y})")

        result = opp_board.receive_shot(x, y)

        # send result to shooter
        send_json(cur_sock, {'type': 'result', 'result': result, 'x': x, 'y': y})

        # notify opponent about incoming shot and result
        try:
            send_json(sockets[opponent], {'type': 'incoming', 'from': names[current], 'x': x, 'y': y, 'result': result})
        except Exception:
            pass

        # check win
        if all_sunk(opp_board):
            print(f"{names[current]} wins!")
            send_json(cur_sock, {'type': 'game_over', 'winner': names[current]})
            send_json(sockets[opponent], {'type': 'game_over', 'winner': names[current]})
            # update leaderboard
            lb = leaderboard()
            lb.update_leaderboard(names[current], names[opponent])

            if msg.get('type') == 'play_again':
                print("Players want to play again. Restarting game.")
                game_loop(srv, clients, players)
                
            break

        turn += 1

    for s in sockets:
        try:
            s.close()
        except Exception:
            pass
    srv.close()


if __name__ == '__main__':
    menu()
