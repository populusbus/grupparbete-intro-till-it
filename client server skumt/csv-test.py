import csv
import os

data = [
    {'name': 'hej', 'wins': 10, 'games': 2},
]

csv_path = 'stats.csv'
fieldnames = ['name', 'wins', 'games']

# Append and write header only if file doesn't exist or is empty
write_header = (not os.path.exists(csv_path)) or os.path.getsize(csv_path) == 0
with open(csv_path, 'a', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    if write_header:
        writer.writeheader()
    writer.writerows(data)

# Read and print file
with open(csv_path, mode='r', encoding='utf-8') as file:
    csvFile = csv.reader(file)
    for lines in csvFile:
        print(lines)