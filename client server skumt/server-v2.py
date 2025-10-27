# ...existing code...
import socket
import csv
import json
import os

on = True
stats = [{'name': 'Nikhil', 'wins': 10, 'games': 2}]

server_ip = 'localhost'
server_port = 9090

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a TCP socket
server.bind((server_ip, server_port))
server.listen(5)  # Listen for incoming connections

fieldnames = ['name', 'wins', 'games']
csv_path = 'stats.csv'

try:
    while True:
        client, addr = server.accept()
        print(f"Connection from {addr}")

        data = client.recv(4096).decode()
        if not data:
            client.close()
            continue

        try:
            payload = json.loads(data)  # expect a dict or list of dicts
        except json.JSONDecodeError:
            client.send(b'ERROR: invalid JSON')
            client.close()
            continue

        # Normalize to list of dicts
        new_entries = []
        if isinstance(payload, dict):
            new_entries = [payload]
        elif isinstance(payload, list):
            new_entries = [p for p in payload if isinstance(p, dict)]
        else:
            client.send(b'ERROR: expected dict or list of dicts')
            client.close()
            continue

        # Append to in-memory stats
        stats.extend(new_entries)
        print(f"Received and appended: {new_entries}")

        # Write new entries to CSV (append mode). Write header if file empty/nonexistent.
        write_header = (not os.path.exists(csv_path)) or os.path.getsize(csv_path) == 0
        with open(csv_path, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if write_header:
                writer.writeheader()
            # Ensure rows include only the expected fields
            for entry in new_entries:
                row = {k: entry.get(k, '') for k in fieldnames}
                writer.writerow(row)
        with open(csv_path, mode='r', encoding='utf-8') as file:
            csvFile = csv.reader(file)
            for lines in csvFile:
                print(lines)

        client.send(f'OK: received {len(new_entries)} entries'.encode())
        client.close()

except KeyboardInterrupt:
    print("Shutting down server.")
finally:
    server.close()
# Read and print file
