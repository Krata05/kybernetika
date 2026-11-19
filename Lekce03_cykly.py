x = 10

while(x > 5):
    print("ahoj")                               #cykly s podminkou na konci a na zacatku
    x = x-1                                     #break = okamzite ukonci cyklus
    if x == 7:                                  #continue = rovnou skoci na dalsi cyklus (preskoci aktualni cyklus)
        break                               #while = dokud platí, cyklus běží (psat si jak to funguje na papir krok za krokem) dalsi zapis x = 10 vypis:ahoj10, 
    print(x)
    

print("konec")


while True:                                                     #nekonecny cyklus, dokud nezmacknu X 
    print("Vyber možnost: A: napis ahoj, X: konec")
    y = input('Zadej volbu:')
    if y == "A":
        print("ahoj")
    if y == "X":
        break


