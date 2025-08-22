secret = 9
quess_count = 1
quess_limit = 3
while quess_count <= quess_limit:
    userQuess = int(input('your quess: '))
    quess_count += 1
    if userQuess == secret:
        print("You won")
        break
else:
    print("Failed")

