# client.py
import socket

server_ip = input("Enter the servers IP adress: ").strip()
server_port = 9090

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a TCP socket

try:
    client.connect((server_ip, server_port))  # Connect to the server. CMD -> ipconfig -> change localhost to ip
    print(f"Connected to server at {server_ip}:{server_port}")

    client.send('Hello from client!'.encode())  # Send data to the server¨
    print("Sent message to server.")

    response = client.recv(1024).decode() # Receive a response from the server
    print(f"Server says: {response}")

except Exception as e:
    print(f"Connection failed: {e}")

finally:
    client.close()
