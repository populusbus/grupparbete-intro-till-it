class Ship:
    def __init__(self, name, length):
        self.name = name
        self.length = length
        self.hits = 0

    def hit(self):
        self.hits += 1
        print(f"{self.name} träffad! ({self.hits}/{self.length})")

    def is_sunk(self):
        """Return True if the ship has been hit at least `length` times.

        This treats any hits >= length as sunk.
        """
        return self.hits >= self.length