class Board:
    def __init__(self, size=10):
        self.size = size
        self.grid = [["~" for _ in range(size)] for _ in range(size)]
        # ships: list of {'ship': Ship, 'positions': [(x,y), ...]}
        self.ships = []

    def place_ship(self, ship, x, y, point):
        """Place a ship on the board.

        - Coordinates (x,y) are 0-indexed, x is column, y is row.
        - point: 'H' or 'V' (horizontal/rightwards or vertical/downwards)
        - Ships are represented on the grid as 'S' and water as '~'.
        Returns True on success, False on failure (out of bounds or overlap).
        """
        length = ship.length
        coords = []

        dir = point.upper()
        if dir == 'H':
            if x + length > self.size:
                print("Skeppet går utanför brädet horisontellt!")
                return False
            coords = [(x + i, y) for i in range(length)]
        elif dir == 'V':
            if y + length > self.size:
                print("Skeppet går utanför brädet vertikalt!")
                return False
            coords = [(x, y + i) for i in range(length)]
        else:
            print("Ogiltig riktning! Använd 'H' eller 'V'.")
            return False

        # Check overlaps
        for cx, cy in coords:
            if self.grid[cy][cx] != "~":
                print("Skeppet överlappar med ett annat skepp!")
                return False

        # Place ship cells as 'S'
        for cx, cy in coords:
            self.grid[cy][cx] = "S"

        # Store ship with its absolute positions
        self.ships.append({"ship": ship, "positions": coords})
        print(f"{ship.name} placerad vid ({x},{y}) riktad {point}")
        return True


    def receive_shot(self, x, y):
        """Process a shot fired at (x,y).

        Returns one of: 'hit', 'miss', 'sunk', 'already', 'invalid'
        Updates this board's grid:
          - 'X' for a hit on a ship
          - 'O' for a miss (water)
        """
        # Bounds check
        if not (0 <= x < self.size and 0 <= y < self.size):
            return 'invalid'

        cell = self.grid[y][x]
        # Already shot here
        if cell in ('X', 'O'):
            return 'already'

        if cell == 'S':
            # hit
            self.grid[y][x] = 'X'
            # find ship containing this coord
            for ship_info in self.ships:
                if (x, y) in ship_info['positions']:
                    ship = ship_info['ship']
                    ship.hit()
                    if ship.is_sunk():
                        print(f"{ship.name} har sänkts!")
                        return 'sunk'
                    return 'hit'
            # If we found 'S' on the grid but no ship record, still treat as hit
            return 'hit'
        else:
            # miss
            self.grid[y][x] = 'O'
            return 'miss'

    # old misspelled name kept for compatibility
    recieve_shot = receive_shot

    def display(self, show_ships=True):
        """Print the board to console.

        show_ships: when False, any 'S' cells are displayed as '~' (useful for opponent view)
        The board is printed with y (rows) as the first index (0..size-1) and x (cols) along the top.
        """
        # Header with x indices
        print("   " + " ".join(f"{i:2}" for i in range(self.size)))
        for y in range(self.size):
            row = []
            for x in range(self.size):
                cell = self.grid[y][x]
                if not show_ships and cell == 'S':
                    row.append('~')
                else:
                    row.append(cell)
            print(f"{y:2} " + " ".join(f"{c:2}" for c in row))


