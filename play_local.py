"""Small hotseat demo showing two players placing ships and firing.

This is a non-networked demo: both players run in the same process and take turns.
Use this to test boards are separate and opponent ships are hidden until hit.
"""
from Player import Player
from Ship import Ship


def demo():
    p1 = Player('Alice', size=5)
    p2 = Player('Bob', size=5)

    # Simple deterministic placement for demo
    p1.place_ship(Ship('Destroyer', 3), 1, 1, 'H')
    p2.place_ship(Ship('Destroyer', 3), 1, 1, 'H')

    # Show initial boards
    print('\nInitial boards:')
    p1.display_boards()
    p2.display_boards()

    # Simulate a few shots: Alice fires then Bob
    rounds = [((1,1),(0,0)), ((2,1),(1,1)), ((3,1),(2,2))]
    for (a_shot, b_shot) in rounds:
        # Alice fires at Bob
        x,y = a_shot
        res = p2.receive_shot(x,y)
        p1.apply_shot_result(x,y,res)
        print(f"Alice fired at ({x},{y}) -> {res}")

        # Bob fires at Alice
        x,y = b_shot
        res = p1.receive_shot(x,y)
        p2.apply_shot_result(x,y,res)
        print(f"Bob fired at ({x},{y}) -> {res}")

        print('\nBoards after round:')
        print("Alice:")
        p1.display_boards()
        print("Bob:")
        p2.display_boards()


if __name__ == '__main__':
    demo()
