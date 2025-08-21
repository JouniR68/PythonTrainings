import math

print("Hello dude")
print("x" * 10)
print("Morot")
x = 1
text = "  python \nprogramming"
first = "Jouni"
last = "Riimala"
# \n
# \'
# \\
print(len(text))
print(text[-1])
print(text[0:3])
print(text[0:])
print(text[:3])
print(text[:])

print(f"{first} {last}")

print(text.title())
print(text)
print(text.rstrip())
print(text.find("Pro"))
print(text.replace("p", "x"))
print("pro" in text)
print("swift" not in text)

print(round(2.9))
print(abs(-2.9))

print(math.ceil(2.2))
print(math.factorial(3))
print(math.log2(20))
print(math.pow(2, 4))
print(math.sqrt(25))

#x = input("x: ")
#y = int(x)+1
#print(f"x: {x}, y: {y}")

# falsy
# ""
# 0
# None

print(bool(0))
print(bool(-1))
print(bool(4))
print(bool("False"))

fruit = "Apple"
print(fruit[1:-1])

print(10 % 3)
ord("B")

temperature = 15
if temperature > 30:
    print("Warm")
elif temperature > 20:
    print("It's nice")
else:
    print("cold")
print("Done")

age = 12
message = "Free to drink and have sex" if age >= 22 else "Go home to grow"
print(message)
