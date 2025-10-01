from random import randint
from textwrap import dedent  # för multirad sträng

turn = 1
shots = 5
shot_at = 0
#targets = [(i, False) for i in range(1, 6)] #list över tuples med (target nummer 1-5, träff värde). kan dock inte ändras senare
targets = {i: False for i in range(1, 6)} # Dictionary med target nummer och dess träff värde
print(targets)

def start():
    print(dedent(f"""\
            ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                       Biathlon
                  a hit or miss game
            ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            
            You have {shots} shots
          """))
    user_input()
    check_hit()
    print_targets(targets)

def user_input():
    global shot_at
    shot_at = int(input(f"Shot nr {turn} at: "))
    
def check_hit():
    random_ = randint(0, 100)

    if random_ > 40:
        targets[shot_at] = True
        print(targets)
    else:
        return

def print_targets(targets):
    for num in targets.keys():
        print(num, end=" ")                             # Skriv ut nycklarna
    print()                                             # Radbryt

    for val in targets.values():
        print("*" if val == False else "O", end=" ")    # Skriv ut värdet
    print()                                         # Radbryt


print_targets(targets)

start()