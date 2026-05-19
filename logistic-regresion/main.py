import random
import math
import numpy as np

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

def skalowanie(x, srednia, odchylenie_standardowe):
    return (x-srednia)/odchylenie_standardowe

def zamiana_na_prawdopodobienstwo(z):
    return 1 / (1 + math.exp(-z))

def oblicz_z(zbior1,zbior2,b):
    if len(zbior1)!=len(zbior2): return None
    result=[]

    for i in range(0,len(zbior1)):
        result.append(zbior1[i]*zbior2[i])
    result.append(b)

    return sum(result)

def regresja_logistyczna(tst,trn):
    avg_war_dla_atrybutow = {}
    for i in range(0,len(trn[0])-1):
        kolumna=[]
        for y in range(0, len(trn)):
            kolumna.append(trn[y][i])
        avg_war_dla_atrybutow[int(i)] = (np.mean(kolumna),np.std(kolumna))

    trn_znormalizowane=[]
    for i in range(0,len(trn)):
        wiersz = []
        for j in range(0,len(trn[i])-1):
            wiersz.append(skalowanie(trn[i][j],avg_war_dla_atrybutow[j][0],avg_war_dla_atrybutow[j][1]))
        wiersz.append(trn[i][-1])
        trn_znormalizowane.append(wiersz)


    wektor_wag = [0.0] * (len(trn[0])-1)
    bias = 0.0
    learning_rate = 0.01
    iteracje = 100

    for i in range(iteracje):
        gradient_wag = [0.0] * (len(trn[0])-1)
        gradient_bias = 0.0

        for j in range(len(trn)):
            xi = trn_znormalizowane[j][:-1]
            yi = trn_znormalizowane[j][-1]

            z = oblicz_z(wektor_wag,xi,bias)

            y_prim = zamiana_na_prawdopodobienstwo(z)

            error = y_prim - yi

            for k in range(len(trn[0])-1):
                gradient_wag[k]+=error*xi[k]

            gradient_bias+=error

        for j in range(len(trn[0])-1):
            gradient_wag[j]=gradient_wag[j]/len(trn)

        gradient_bias=gradient_bias/len(trn)

        for j in range(len(trn[0])-1):
            wektor_wag[j]=wektor_wag[j]-learning_rate*gradient_wag[j]

        bias=bias-learning_rate*gradient_bias

    tst_znowmalizowane=[]
    for i in range(0, len(tst)):
        wiersz = []
        for j in range(0, len(tst[i]) - 1):
            wiersz.append(skalowanie(tst[i][j], avg_war_dla_atrybutow[j][0], avg_war_dla_atrybutow[j][1]))
        wiersz.append(tst[i][-1])
        tst_znowmalizowane.append(wiersz)

    przewidziane=[]
    for i in range(len(tst_znowmalizowane)):
        xi=tst_znowmalizowane[i][:-1]
        z=oblicz_z(wektor_wag,xi,bias)
        y_prim = zamiana_na_prawdopodobienstwo(z)
        if y_prim >=0.5:
            przewidziane.append(1)
        else:
            przewidziane.append(0)

    return przewidziane

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
    dane = get_data("australian 1.csv")
    kafelki = kross_walidacja(dane)
    ogolne_accuracy = []

    for numer_kafla in range(6):
        print(f'\n---------------Iteracja {numer_kafla+1}-------------------')

        zbior_testowy = kafelki[numer_kafla]
        zbiory_treningowe = []

        for i in range(6):
            if i != numer_kafla:
                for obiekt in kafelki[i]:
                    zbiory_treningowe.append(obiekt)

        przewidziane = regresja_logistyczna(zbior_testowy,zbiory_treningowe)
        rzeczywiste  = [klasa[-1] for klasa in zbior_testowy]

        accuracy = macierz_pomylek(przewidziane,rzeczywiste)
        ogolne_accuracy.append(accuracy)

    srednia = sum(ogolne_accuracy) / len(ogolne_accuracy)
    print(f"\n---------------Srednie accuracy: {srednia}-------------------")

main()