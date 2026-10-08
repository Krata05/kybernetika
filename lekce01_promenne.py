cislo = 11 # = prirazzuje hodnotu promenne
pocet_kusu_dobytka = 3

print(pocet_kusu_dobytka)
print(type(pocet_kusu_dobytka))

# aritmeticke operace +, -, *, %, /, //, **

nevim = cislo / pocet_kusu_dobytka # deleni
print(nevim)
print(type(nevim))

nevim = cislo // pocet_kusu_dobytka # celociselne deleni
print(nevim)
print(type(nevim))

nevim = cislo % pocet_kusu_dobytka #zbytek po celociselnem deleni
print(nevim)
print(type(nevim))

nevim = cislo ** pocet_kusu_dobytka # mocnina
print(nevim)
print(type(nevim))

nevim = cislo ** (1/pocet_kusu_dobytka) # odmocnina
print(nevim)
print(type(nevim))