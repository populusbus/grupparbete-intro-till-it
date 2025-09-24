def flippblipp(n):
    if n%3==0 and n%5==0:
        return "flipp blipp"
    elif n%3==0:
        return "flipp"
    elif n%5==0:
        return "blipp"
    else:
        return n
gaming = True
x=1
print(str(flippblipp(x)))
while gaming==True:
    x+=1
    uInput=input("Nästa: ")
    if uInput==str(flippblipp(x)):
        continue
    else:
        print("Fel! - " + str(flippblipp(x)))
        gaming=False



