a = float(input("Zadej stranu a: "))
b = float(input("Zadej stranu b: "))
c = float(input("Zadej stranu c: "))

spravnost = a + b > c and a + c > b and b + c > a
if spravnost:
    print("Trojúhelník je sestrojitelný.")
else:
    print("Trojúhelník není sestrojitelný.")