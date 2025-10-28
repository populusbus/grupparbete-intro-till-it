from Board import Board


class Player:
    def __init__(self, name="Player", size=10):
        self.name = name
        # Own board stores ships and all own markers
        self.own_board = Board(size)
        # Opponent board stores only what this player knows about opponent (shots)
        self.opponent_board = Board(size)

    def place_ship(self, ship, x, y, point):
        """Place a ship on the player's own board.

        Returns True on success, False on failure.
        """
        return self.own_board.place_ship(ship, x, y, point)

    def display_your_board(self):
        """Display only the player's own board."""
        print(f"=== {self.name} - Own board ===")
        self.own_board.display(show_ships=True)

    def display_boards(self, opponent_name="Opponent"):
        """Display own board (left) and opponent known board (right).

        For quick console viewing we print them sequentially.
        """
        print(f"=== {self.name} - Own board ===")
        self.own_board.display(show_ships=True)
        print(f"=== {opponent_name} - Opponent view ===")
        # opponent_board does not have ships placed, but may have X/O markers
        self.opponent_board.display(show_ships=False)

    def fire(self, x, y):
        """Return coordinates to fire at. Networking or game-loop will call this.

        This method does not contact the opponent. It simply provides coordinates as a
        compact API point. The caller should send/route the shot to the opponent and
        then call `apply_shot_result` with the result.
        """
        return (x, y)

    def apply_shot_result(self, x, y, result):
        """Apply the result of a shot fired at opponent to this player's opponent_board.

        result is one of: 'hit', 'miss', 'sunk', 'already', 'invalid'
        """
        if result == 'hit' or result == 'sunk':
            self.opponent_board.grid[y][x] = 'X'
        elif result == 'miss':
            self.opponent_board.grid[y][x] = 'O'
        # ignore 'already'/'invalid'

    def receive_shot(self, x, y):
        """Convenience wrapper to let opponent fire at this player's own board.

        Returns the same codes as Board.receive_shot.
        """
        return self.own_board.receive_shot(x, y)
