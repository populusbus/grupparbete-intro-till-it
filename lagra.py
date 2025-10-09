#användare
users = {
    "nisse": ["1234","äpple", "banan"],
    "adam": ["abcd","fisk", "hamster"]
}


def start():
    print("Welcome to Lagra (TM)\n" \
    "1. Log in\n" \
    "2. Quit\n" )
    val = input("Option: ")
    if val == "1":
        login()
    elif val == "2":
        exit
    else:
        print("Invalid option")
        start()

def login():
    name = input("\nUsername: ")
    password = input("Password: ")
    if name in users and users[name][0] == password:
        print(f"\nWelcome {name}")
        menu(name)
    else:
        print("\nLogin failed")
        val=input("1) Try again\n2) Quit\nOption: ")
        if val == "1":
            login()
        else:
            start()

def menu(name):
    print("\nselect an option:")
    val=input("1) View items\n2) Add item\n3) Logout\nOption: ")
    if val == "1":
        print("\nYour items:")
        for item in users[name][1:]:
            num=1
            print(f"{num}) {item}")
        menu(name)
    elif val == "2":
        item = input("Enter item to add: ")
        users[name].append(item)
        print(f"\nItem '{item}' added.")
        menu(name)
    elif val == "3":
        print("Logging out...")
        start()
    else:
        print("Invalid option")
        menu(name)
          
start()