print("Program, um Zahlen der Größe nach zu sortieren")

Z1 = int(input("Zahl 1: "))
Z2 = int(input("Zahl 2: "))

tmp = 0

if Z1 > Z2:
    tmp = Z1
    Z1 = Z2
    Z2 = tmp

print(Z1,Z2)