#uloha 3: uzivatel zada cislo a program vypise cisla od nuly do zadaneho cisla, ale jen cisla suda (nula je suda)

a = int(input("Napiš číslo: "))
for i in range(0, a + 1, 2):
    print(i)


 #takhle to jde taky zapsat 
for i in range(a+1):
    if i%2 == 0:
        print(i)


#nebo takhle
for i in range(int(a/2)+1):
    print(2*i)



