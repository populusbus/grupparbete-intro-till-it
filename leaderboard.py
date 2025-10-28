import csv
import os
import json
import random
LEADERBOARD_FILE = 'leaderboard.csv'
def load_leaderboard():
    leaderboard = {}
    if os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                name, wins, losses = row
                leaderboard[name] = {'wins': int(wins), 'losses': int(losses)}
    return leaderboard

def save_leaderboard(leaderboard):
    with open(LEADERBOARD_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        for name, record in leaderboard.items():
            writer.writerow([name, record['wins'], record['losses']])

def update_leaderboard(winner_name, loser_name):
    leaderboard = load_leaderboard()

    if winner_name not in leaderboard:
        leaderboard[winner_name] = {'wins': 0, 'losses': 0}
    if loser_name not in leaderboard:
        leaderboard[loser_name] = {'wins': 0, 'losses': 0}

    leaderboard[winner_name]['wins'] += 1
    leaderboard[loser_name]['losses'] += 1

    save_leaderboard(leaderboard)

def display_leaderboard():
    leaderboard = load_leaderboard()

    option=input("1. Sort by Wins\n2. Sort by Losses\n3. Sort by winrate\nChoose an option (1 or 2): ")
    if option=='2':
        sorted_leaderboard = sorted(leaderboard.items(), key=lambda item: item[1]['losses'], reverse=True)
    elif option=='3':
        sorted_leaderboard = sorted(leaderboard.items(), key=lambda item: (item[1]['wins']/(item[1]['wins']+item[1]['losses']) if (item[1]['wins']+item[1]['losses'])>0 else 0), reverse=True) 
    elif option=='1':
        sorted_leaderboard = sorted(leaderboard.items(), key=lambda item: item[1]['wins'], reverse=True)
    else:
        print("Invalid option. Displaying by Wins.")
    print("=== Leaderboard ===")
    print(f"{'Player':<20} {'Wins':<5} {'Losses':<7}")
    print("-" * 34)
    for name, record in sorted_leaderboard:
        print(f"{name:<20} {record['wins']:<5} {record['losses']:<7}")
    print("===================")
names=['Alice', 'Bob', 'Charlie', 'Diana']
for _ in range(10):
    winner, loser = random.sample(names, 2)
    update_leaderboard(winner, loser)

display_leaderboard()