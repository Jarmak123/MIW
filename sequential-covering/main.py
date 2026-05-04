from itertools import combinations

def get_data(name_of_file):
    result = []

    with open(name_of_file, "r") as f:
        for line in f:
            row = [int(x) for x in line.split()]
            result.append(row)

    naglowek=[]
    for i in range(1, len(result[0])):
        naglowek.append("a"+str(i))
    naglowek.append("d")
    result.insert(0,naglowek)

    return result

def print_data(data):
    print("     a1", "a2", "a3", "a4", "a5", "a6", "d")
    for i in range(1, len(data)):
        print(f'o{i}: {data[i]}')

def zbiory(data, liczebnosc):
    zbiory=[]
    for i in data:
        temp = i[:-1]
        zbior = list(combinations(temp, liczebnosc))
        zbior.append(i[-1])
        zbiory.append(zbior)

    return zbiory

def znajdz_sprzeczne(data):
    sprzeczne = []
    for i in range(1, len(data)):
        for y in range(1, len(data)):
            if i == y: continue
            atrybuty_i = data[i][:-1]
            atrybuty_y = data[y][:-1]
            if atrybuty_i == atrybuty_y and data[i][-1] != data[y][-1]:
                if i not in sprzeczne:
                    sprzeczne.append(i)
    return sprzeczne

def main():
    data = get_data("data.txt")
    print_data(data)

    sprzeczne = znajdz_sprzeczne(data)
    if sprzeczne:
        print(f"\nObiekty sprzeczne (pomijamy): {['o'+str(s) for s in sprzeczne]}")

    pokrycie = []
    reguly = []
    rzad = 1

    do_pokrycia = []

    for i in range(1, len(data)):
        if i not in sprzeczne: do_pokrycia.append(i)

    while len(pokrycie) < len(do_pokrycia):
        print(f"\nRząd {rzad}:")
        zbior = zbiory(data, rzad)
        naglowek_combo = zbior[0]
        znaleziono_w_rzedzie = False

        for i in range(1, len(zbior)):
            if i in pokrycie or i in sprzeczne: continue

            decyzja = zbior[i][-1]
            znaleziono = False

            for j in range(0, len(zbior[i]) - 1):
                etykieta = naglowek_combo[j]
                wartosc = zbior[i][j]

                unikat = True
                temp_pokrycie = []

                for y in range(1, len(zbior)):
                    if zbior[y][j] == wartosc and y == i:
                        continue
                    if zbior[y][j] == wartosc:
                        if zbior[y][-1] != decyzja:
                            unikat = False
                            break
                        temp_pokrycie.append(y)

                if unikat:
                    temp_pokrycie.append(i)
                    nowe = [p for p in temp_pokrycie if p not in pokrycie]
                    support = len(temp_pokrycie)

                    regula=""
                    if rzad > 1:
                        regula_czesc=[]
                        for etykieta, wartosc in zip(etykieta, wartosc):
                            regula_wyjscie=f"({etykieta}={wartosc})"
                            regula_czesc.append(regula_wyjscie)
                        regula = " ^ ".join(regula_czesc)
                    else:
                        regula = f"({etykieta[0]}={wartosc[0]})"

                    support_wyjscie = ""
                    if support > 1: support_wyjscie = f"[{support}]"
                    else: support_wyjscie = ""

                    print(f"  z o{i}: {regula} => (d={decyzja}){support_wyjscie} wyrzucamy: {['o'+str(p) for p in nowe]}")

                    reguly.append((regula, decyzja, support))
                    for p in nowe:
                        pokrycie.append(p)

                    znaleziono = True
                    break

            if not znaleziono:
                print(f"  z o{i}: brak")

        rzad += 1

    print("\nZnalezione reguly:")
    for regula, decyzja, support in reguly:
        support_wyjscie = f"[{support}]" if support > 1 else ""
        print(f"  {regula} => (d={decyzja}){support_wyjscie}")

main()