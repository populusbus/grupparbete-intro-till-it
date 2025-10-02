from random import randint
from textwrap import dedent  # för multirad sträng

turn = 0
shots = 5
shot_at = 0
#targets = [(i, False) for i in range(1, 6)] #list över tuples med (target nummer 1-5, träff värde). kan dock inte ändras senare
targets = {i: False for i in range(1, 6)} # Dictionary med target nummer och dess träff värde


def start():
    global turn2, shots2, shot_at2, targets2
    turn2 = turn
    shots2 = shots
    shot_at2 = shot_at
    targets2 = targets.copy()
    print(dedent(f"""\
            ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                       Biathlon
                  a hit or miss game
            ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            
            You have {shots} shots
          """))
    print_targets(targets)
    next_turn()

def user_input():
    global shot_at
    shot_at = int(input(f"Shot nr {turn} at: "))
    
def check_hit():
    random_ = randint(0, 100)

    if random_ > 40:
        if targets[shot_at] == False:  # kolla om målet är öppet
            print("Hit on open target!")
            targets[shot_at] = True
        else:
            print("Hit on closed target!")
    else:
        print("Miss!")
        return

def print_targets(targets):
    for num in targets.keys():
        print(num, end=" ")                             # Skriv ut nycklarna
    print()                                             # Radbryt

    for val in targets.values():
        print("*" if val == False else "O", end=" ")    # Skriv ut värdet
    print()                                         # Radbryt

def next_turn():
    global turn, shots, shot_at, targets
    turn += 1
    if turn <= shots:
        user_input()
        check_hit()
        print_targets(targets)
        next_turn()
    else:
        print(f"You hit {sum(targets.values())} out of {len(targets)} targets!") # summera alla True värden i dictionaryn
        again=input("Do you want to play again? (y/n) ")
        if again.lower() == "y":
            turn = turn2
            shots = shots2
            shot_at = shot_at2
            targets = targets2.copy()
            start()
        else:
            print("Thanks for playing!")
            exit()
    

start()