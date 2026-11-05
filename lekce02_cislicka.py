vstup = int(input("Zadej číslo: "))
cislo = vstup % 2

if cislo == 1:
    print(f"{vstup} je liché číslo.")
else:
    print(f"{vstup} je sudé číslo.")
