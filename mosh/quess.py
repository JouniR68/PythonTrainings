secret = 9
i = 1

while i <= 3:
    userQuess = int(input('your quess: '))
    if userQuess == secret:
        print("You won")
        break
    i = i + 1
print("Game over")
