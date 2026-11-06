polomer = float(input("Zadej r: "))
vyska = float(input("Zadej v: "))

from math import pi
from decimal import Decimal, ROUND_HALF_UP

y = (polomer ** 2 + vyska ** 2) ** (1/2)

V = 1/3 * pi * polomer ** 2 * vyska
Vz = float(Decimal(str(V)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))
print(f"Objem je {Vz} cm3.")

S = pi * polomer ** 2 + pi * polomer * y
Sz = float(Decimal(str(S)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))
print(f"Povrch je: {Sz} cm2.")