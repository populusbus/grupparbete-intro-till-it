import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a TCP socket
client.connect(('localhost', 8080))  # Connect to the server

client.send('Hello from client!'.encode())  # Send data to the server¨
print("TRIED SENDING REQUEST")
print(client.recv(1024).decode())  # Receive a response from the server
print("TRIED RECIVING REQUEST")