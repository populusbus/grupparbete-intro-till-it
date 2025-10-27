# client.py
import socket
import json

server_ip = 'localhost'
server_port = 9090

name = 'test'
games = 100
wins = 5

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client.connect((server_ip, server_port))
    print(f"Connected to server at {server_ip}:{server_port}")

    stats = {'name': name, 'games': games, 'wins': wins}
    client.send(json.dumps(stats).encode())
    print("Sent JSON message to server.")

    response = client.recv(1024).decode()
    print(f"Server says: {response}")

except Exception as e:
    print(f"Connection failed: {e}")

finally:
    client.close()