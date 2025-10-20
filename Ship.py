class Ship:
    def __init__(self, name, length):
        self.name = name
        self.length = length
        self.hits = 0

    def hit(self):
        self.hits += 1
        print(f"{self.name} träffad! ({self.hits}/{self.length})")

    def is_sunk(self):
        pass