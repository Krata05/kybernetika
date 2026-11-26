# uloha 1: vytvorte list o libovolnych 5 cislech a pomoci for-cyklu spocitejte pocet cisel v cyklu
# soucet nakonec vypiste

muj_list = [17, 13, 12, 1, 30]


soucet = 0
for i in range(len(muj_list)):
    soucet = soucet + muj_list[i]

print(soucet)

# uloha 2: vytvo list 5 libovolnych cisel a seznam pomoci for-cyklu vypiste v opacnem poradi
print(10*"*")


muj_list = [1, 2, 3, 4, 5]

for i in range(len(muj_list)-1,-1,-1):      # range(zacatek vcetne, konec neni vcetne, krok) <a,b)
    print(muj_list[i])



# uloha 3: vytvorte list 5 libovolnych cisel a spocitejte pomoci for-cyklu jejich aritmetický prumer
print(10*"*")


muj_list = [1, 1, 4, 5, 3]

soucet = 0

for i in range(len(muj_list)):      # x = x + 1 to same je x+ = 1
    soucet += muj_list[i]

prumer = soucet / len(muj_list)

print(f"prumer = {prumer}")


# uloha 4: vytvorte list 5 libovolnych cisel a vypiste nejvyssi  cislo ze seznamu
print(10*"*")

muj_list = [1, 4, 6, 17, 7]

max = muj_list[0]
for i in range(len(muj_list)):
    if muj_list[i] > max:
        max = muj_list[i]

print(f"maximum je: {max}")

muj_list = ["nazdar", "ahoj", "cau"]



for i in range(len(muj_list)-1):
    print(str(i) + " " + muj_list[i])
    print(muj_list[i+1])

for item in muj_list:
    print(item)


#uloha 5: vytvorte list 5 libovolnych cisel a vypiste nejvyssi  cislo ze seznamu
print(10*"*")


muj_list = [1, 4, 6, 17, 7]

if muj_list[0] > muj_list[1]:
    nejvetsi = muj_list[0]
    druhy_nejvetsi = muj_list[1]
else:
    nejvetsi = muj_list[1]
    druhy_nejvetsi = muj_list[0]

for i in range(2,  len(muj_list)):
    if muj_list[i] > nejvetsi:
        druhy_nejvetsi = nejvetsi
        nejvetsi = muj_list[i]
    elif muj_list[i] > druhy_nejvetsi:
        druhy_nejvetsi = muj_list[i]

