# converter
import math

paino = input("paino: ")
unit = input("Unit l vai k:")

print(f"Annoit arvot: {paino} {unit} ")

if unit.upper() == "k":
    print(f"Painosi kiloina = {round(float(paino) * 0.45)}")
else:
    print(f"Painosi poundeina: {round(float(paino)/0.45)}")
