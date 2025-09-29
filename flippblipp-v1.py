n=15

# Loopar från 1 till och med n
for i in range(1, 1 + n):
    if i % 3 == 0 and i % 5 == 0:
        print("flipp blipp")
    elif i % 3 == 0:
        print("flipp")
    elif i % 5 == 0:
        print("blipp")
    else:
        print(i)