# server.py
import socket
import csv

on=True
stats=[{'name': 'Nikhil', 'wins': 10, 'games': 2}]
def get_local_ip():
    """Finds the local ip adress on this machine (LAN adress)."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close
    return ip


server_ip = 'localhost'
server_port = 9090

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)# Create a TCP socket
# server.bind(('localhost', 8080))# Bind the socket to an address and port
server.bind((server_ip, server_port))

server.listen(5)# Listen for incoming connections

while on==True:
    client, addr = server.accept()# Accept a connection
    print(f"Connection from {addr}")
    statsL=len(stats)
    stats += client.recv(1024).decode()
    print(f"Client says: {stats}")# Print the client response

    # print("TRIED RECIVING RESPONSE")
    client.send(f'Hello from server!{stats}'.encode())# Send a response to the client
    print("Sent response to client\n")
    client.close()
    if statsL != stats.len:
        on=False


with open('stats.csv', 'w', newline='') as csvfile:
    fieldnames = ['name', 'branch', 'year', 'cgpa']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(stats)
