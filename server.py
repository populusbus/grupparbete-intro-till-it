# server.py
import socket

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


server_ip = get_local_ip()
server_port = 9090

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)# Create a TCP socket
# server.bind(('localhost', 8080))# Bind the socket to an address and port
server.bind((server_ip, server_port))

server.listen(5)# Listen for incoming connections

while True:
    client, addr = server.accept()# Accept a connection
    print(f"Connection from {addr}")

    message = client.recv(1024).decode()
    print(f"Client says: {message}")# Print the client response

    # print("TRIED RECIVING RESPONSE")
    client.send('Hello from server!'.encode())# Send a response to the client
    print("Sent response to client\n")

    client.close()