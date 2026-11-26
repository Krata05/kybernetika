#uloha 4: uzivatel zada cislo a program vypise cisla od nuly do zadaneho cisla (vcetne) 
# a k tomu vypise. zda je aktualni cislo sude nebo liche


a = int(input("Napiš číslo: "))

for i in range(a+1):
    print(i)
    if i % 2 == 0:
        print(str(i) + " je sudé.")
    else: 
        print(f"{i} je liché.")











