import random
import math
import numpy as np

def get_data(name_of_file):
    result = []

    with open(name_of_file, "r") as f:
        for line in f:
            row = []
            for x in range(0,len(line.strip().split(','))):
                if x == len(line.strip().split(','))-1: row.append(line.strip().split(',')[x])
                else: row.append(float(line.strip().split(',')[x]))
            result.append(row)

    return result

def print_data(data):
    for i in range(0, len(data)):
        print(data[i])

def policz_p_od_c(c):
    slownik={}
    unikat_klasy=[]
    for i in c:
        if i[-1] not in unikat_klasy: unikat_klasy.append(i)

    for x in unikat_klasy:
        temp_licznik=0
        for y in range(0,len(c)):
            if c[y][-1]==x: temp_licznik+=1

        slownik[x] = temp_licznik/len(c)

    return slownik

def utworz_stat_klas(c):
    slownik={}
    unikat_klasy = []
    for i in c:
        if i[-1] not in unikat_klasy: unikat_klasy.append(i)

    for x in unikat_klasy:
        for y in range(0,len(c)):
            elementy_atrybutu = []
            if x != c[y][-1]: continue
            for j in range(0,len(c[y])):
                for i in (0, len(c)):
                    elementy_atrybutu.append(c[i][j])
        slownik[x]=(np.mean(elementy_atrybutu),np.var(elementy_atrybutu))

    return slownik

def kross_walidacja(dane):
    kafelki=[]
    obecne=[]
    temp = []
    licznik=0
    while(licznik!=len(dane)):
        j = random.randint(0,149)
        if j not in obecne:
            obecne.append(j)
            licznik=licznik+1
            temp.append(dane[j])
            if len(temp)==30:
                kafelki.append(temp)
                temp=[]

    return kafelki

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

def policz_dla_kazdego(war, atrybut,srednia):
    dol_ulamka = math.sqrt(2*math.pi*war**2)
    do_potegi = -1*((atrybut-srednia)**2/(2*war**2))
    razem = 1/dol_ulamka * math.e**do_potegi
    return razem

def main():
    data = get_data("iris.data")
    print_data(data)
    kafelki=kross_walidacja(data)
    print_data(kafelki)

    np.log()
main()