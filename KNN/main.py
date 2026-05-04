import random
import math

def get_data(name_of_file):
    result = []

    with open(name_of_file, "r") as f:
        for line in f:
            row = [float(x) for x in line.split()]
            result.append(row)

    return result

def print_data(data):
    for i in range(0, len(data)):
        print(data[i])

def eukiledes(zbiorA, zbiorB):
    if len(zbiorA) != len(zbiorB): return None
    result = 0
    for i in range(len(zbiorA)-1):
        result += (zbiorA[i] - zbiorB[i]) ** 2

    return math.sqrt(result)

def kross_walidacja(dane):
    kafelki=[]
    obecne=[]
    temp = []
    licznik=0
    while(licznik!=len(dane)):
        j = random.randint(0,689)
        if j not in obecne:
            obecne.append(j)
            licznik=licznik+1
            temp.append(dane[j])
            if len(temp)==115:
                kafelki.append(temp)
                temp=[]

    return kafelki

def najwieksze_tulpy(tulp, rozmiar):
    tulp.sort(key=lambda x: x[0])
    return tulp[:rozmiar]

def knn(k, tst, trn):
    przewidziane_klasy = []

    for i in range(len(tst)):
        dystanse=[]
        for j in range(len(trn)):
            dystanse.append((eukiledes(tst[i], trn[j]),trn[j][-1]))

        najblizsze_klasy = najwieksze_tulpy(dystanse, k)

        zera = 0
        jedynki = 0
        for i in najblizsze_klasy:
            if i[1] == 0.0: zera+=1
            elif i[1] == 1.0: jedynki+=1

        if zera>jedynki: przewidziane_klasy.append(0)
        elif jedynki>zera: przewidziane_klasy.append(1)
        else: przewidziane_klasy.append(None)

    return przewidziane_klasy

def macierz_pomylek(przewidzne,rzecziwiste):
    #true/false | posivite/negative
    #przewidzenie | rzeczywistosc
    tp = 0
    tn = 0
    fp = 0
    fn = 0

    for i in range(len(rzecziwiste)):
        r = rzecziwiste[i]
        p = przewidzne[i]

        if p == None: continue
        elif r == 1 and p == 1: tp += 1
        elif r == 0 and p == 0: tn += 1
        elif r == 0 and p == 1: fp += 1
        elif r == 1 and p == 0: fn += 1


    accuracy = (tp+tn) / len(rzecziwiste)

    print(f"macierz pomylek:")
    print(f"              rzeczywiste 0:  rzeczywiste 1:")
    print(f"przewidziane 0:   {tn}         {fn}")
    print(f"przewidziane 1:   {fp}         {tp}")
    print(f"accuracy:{accuracy}")

    return accuracy

def main():
    dane = get_data("australian.csv")
    kafelki = kross_walidacja(dane)
    k=3
    ogolne_accuracy = []

    for numer_kafla in range(6):
        print(f'\n---------------Iteracja {numer_kafla+1}-------------------')

        zbior_testowy = kafelki[numer_kafla]
        zbiory_treningowe = []

        for i in range(6):
            if i != numer_kafla:
                for obiekt in kafelki[i]:
                    zbiory_treningowe.append(obiekt)

        przewidziane = knn(k, zbior_testowy, zbiory_treningowe)
        rzeczywiste  = [klasa[-1] for klasa in zbior_testowy]

        accuracy = macierz_pomylek(przewidziane,rzeczywiste)
        ogolne_accuracy.append(accuracy)

    srednia = sum(ogolne_accuracy) / len(ogolne_accuracy)
    print(f"\n---------------Srednie accuracy: {srednia}-------------------")

main()