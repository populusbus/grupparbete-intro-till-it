#användare
users = {
    "nisse": ["1234","äpple", "banan"],
    "adam": ["abcd","fisk", "hamster"]
}


def start():
    val = menu_choice("Welcome to Lagra (TM)\n1. Log in\n2. Quit", ["1", "2"])
    if val == "1":
        login()
    elif val == "2":
        exit()


def login():
    name = input("\nUsername: ")
    password = input("Password: ")
    if name in users and users[name][0] == password: # kolla om användarnamn finns och om lösenord stämmer
        print(f"\nWelcome {name}")
        menu(name)
    else:
        print("\nLogin failed")
        val = menu_choice("1) Try again\n2) Quit", ["1", "2"])
        if val == "1":
            login()
        elif val == "2":
            start()


def menu(name):
    print("\nSelect an option:")
    val = menu_choice("1) View items\n2) Add item\n3) Remove item\n4) Logout", ["1", "2", "3", "4"])

    if val == "1":
        print("\nYour items:")
        for i, item in enumerate(users[name][1:], start=1): # hoppa över första elementet som är lösenord
            print(f"{i}) {item}")
        menu(name)
    elif val == "2":
        item = input("Enter item to add: ")
        users[name].append(item)
        print(f"\nItem '{item}' added.")
        menu(name)
    elif val == "3":
        remove_item(name)
    elif val == "4":
        print("Logging out...")
        start()


def remove_item(name):
    items = users[name][1:]
    if not items:
        print("You have no items to remove")
        menu(name)
        return
    
    print("\nYour items")
    for i, item in enumerate(items, start=1):
        print(f"{i}) {item}")
    
    valid_choices = [str(i) for i in range(1, len(items) + 1)]
    item_to_remove = menu_choice("Enter number of item to remove: ", valid_choices)

    removed = users[name].pop(int(item_to_remove))
    print(f"\nItem '{removed}' removed.")

    menu(name)


def menu_choice(prompt, options):
    print(prompt)
    
    val = input("\nOption: ")
    while val not in options:
        print("\nInvalid option")
        val = input("Option: ")

    return val


start()