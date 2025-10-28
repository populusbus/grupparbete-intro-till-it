import socket
import json
from Board import Board
from Ship import Ship


def recv_json(sock):
    data = b''
    while True:
        chunk = sock.recv(4096)
        if not chunk:
            return None
        data += chunk
        # try split by newline
        if b'\n' in data:
            line, rest = data.split(b'\n', 1)
            # put rest back into a buffer by prepending to next recv (simple protocol: one message per line)
            try:
                return json.loads(line.decode())
            except json.JSONDecodeError:
                return None


def send_json(sock, obj):
    msg = (json.dumps(obj) + '\n').encode()
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
            break

        turn += 1

    for s in sockets:
        try:
            s.close()
        except Exception:
            pass
    srv.close()


if __name__ == '__main__':
    run_server()
