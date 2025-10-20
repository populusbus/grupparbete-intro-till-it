class Board:
    def __init__(self, size=10):
        self.size = size
        self.grid = [["~" for _ in range(size)] for _ in range(size)]
        self.ships = []

    def place_ship(self, ship, x, y, point):
        self.ships.append(ship)
        print(f"{ship} placerad vid ({x},{y}) riktad {point}")
