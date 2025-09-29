x=30

# Funktion som tar in talet n och returnerar flipp blipp värde
def flippblipp(n):
    if n % 3 == 0 and n % 5 == 0:
        return "flipp blipp"
    elif n % 3 == 0:
        return "flipp"
    elif n % 5 == 0:
        return "blipp"
    else:
        return str(n)

for i in range(1, 1 + x):
    print(flippblipp(i))
            

