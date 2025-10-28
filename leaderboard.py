import csv
import os

class leaderboard:
    def __init__(self):
        self.LEADERBOARD_FILE = 'leaderboard.csv'

    def load_leaderboard(self):
        leaderboard = {}
        if os.path.exists(self.LEADERBOARD_FILE):
            with open(self.LEADERBOARD_FILE, mode='r', newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    name, wins, losses, winrate = row
                    leaderboard[name] = {'wins': int(wins), 'losses': int(losses), 'winrate': float(winrate)}
        return leaderboard

    def save_leaderboard(self, leaderboard):
        with open(self.LEADERBOARD_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            for name, record in leaderboard.items():
                writer.writerow([name, record['wins'], record['losses'], (record['wins']/(record['wins']+record['losses']) if (record['wins']+record['losses'])>0 else 0)])

    def update_leaderboard(self, winner_name, loser_name):
        leaderboard = self.load_leaderboard()

        if winner_name not in leaderboard:
            leaderboard[winner_name] = {'wins': 0, 'losses': 0 ,'winrate':0}
        if loser_name not in leaderboard:
            leaderboard[loser_name] = {'wins': 0, 'losses': 0,'winrate':0}

        leaderboard[winner_name]['wins'] += 1
        leaderboard[loser_name]['losses'] += 1
        leaderboard[winner_name]['winrate']=(leaderboard[winner_name]['wins']/(leaderboard[winner_name]['wins']+leaderboard[winner_name]['losses']))
        leaderboard[loser_name]['winrate']=(leaderboard[loser_name]['wins']/(leaderboard[loser_name]['wins']+leaderboard[loser_name]['losses']))

        self.save_leaderboard(leaderboard)

    def display_leaderboard(self):
        leaderboard = self.load_leaderboard()

        option=input("1. Sort by Wins\n2. Sort by Losses\n3. Sort by winrate\nChoose an option (1, 2 or 3): ")
        if option=='2':
            sorted_leaderboard = sorted(leaderboard.items(), key=lambda item: item[1]['losses'], reverse=True)
        elif option=='3':
            sorted_leaderboard = sorted(leaderboard.items(), key=lambda item: (item[1]['wins']/(item[1]['wins']+item[1]['losses']) if (item[1]['wins']+item[1]['losses'])>0 else 0), reverse=True) 
        elif option=='1':
            sorted_leaderboard = sorted(leaderboard.items(), key=lambda item: item[1]['wins'], reverse=True)
        else:
            print("Invalid option. Displaying by Wins.")
        print("=== Leaderboard ===")
        print(f"{'Player':<20} {'Wins':<5} {'Losses':<7} {'Winrate':<8}")
        print("-" * 34)
        for name, record in sorted_leaderboard:
            print(f"{name:<20} {record['wins']:<5} {record['losses']:<7} {round((record['winrate'])*100, 2):4}%")
        print("===================")
