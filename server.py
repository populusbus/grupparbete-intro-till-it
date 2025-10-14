import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)# Create a TCP socket
server.bind(('localhost', 8080))# Bind the socket to an address and port

server.listen(5)# Listen for incoming connections

while True:
    client, addr = server.accept()# Accept a connection
    print(client.recv(1024).decode())# Print the client response
    print("TRIED RECIVING RESPONSE")
    client.send('Hello from server!'.encode())# Send a response to the client
    print("TRIED SENDING RESPONSE")