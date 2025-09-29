x=1
gaming = True

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


print(flippblipp(x))

while gaming: # så länge spelet är igång
    x += 1
    uInput = input("Nästa: ")
    
    if uInput == flippblipp(x):
        continue
    else:
        print("Fel! Rätt svar var: " + flippblipp(x))
        print(f"Du klarade {x - 1} steg.")
        break



