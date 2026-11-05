vstup = input("Zadej ňeco: ")

print(vstup)
print(type(vstup)) #vzdy string, protoze input() vraci string

vstup1 = input("Zadej číslo: ")
vstup2 = input("Zadej číslo: ")

cislo1 = int(vstup1) #int je cele cislo, float je desetinne cislo
cislo2 = float(vstup2)
vysledek = cislo1 + cislo2
v = vstup1 + vstup2

print("Součet čísel je: " + str(vysledek))
print("Součet stringu je: " + v)


print(f"Součet čísel je: {vysledek}")

print("Souccet cisel: {}.".format(vysledek)) #format je stara metoda, f-string je nova metoda pro vice promenych