vstup = input("Zadej věk: ")
vek = int(vstup)

if vek >= 18:
    print("Jsem dospělý")
    print("Je ti " + str(vek) + " let.")
else:
    print("Jsem ještě dítě")
    chybi = 18 - vek
   
    if chybi == 1:
        print(f"Do dospělosti ti chybí {chybi} rok.")
    elif chybi < 5:
        print(f"Do dospělosti ti chybí {chybi} roky.")
    else:
        print(f"Do dospělosti ti chybí {chybi} let.")
