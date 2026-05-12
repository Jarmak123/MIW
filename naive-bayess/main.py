import random
import math
import numpy as np

def get_data(name_of_file):
    result = []

    with open(name_of_file, "r") as f:
        for line in f:
            row = []
            for x in range(0, len(line.strip().split(','))):
                if x == len(line.strip().split(',')) - 1: row.append(line.strip().split(',')[x])
                else: row.append(float(line.strip().split(',')[x]))
            result.append(row)

    return result

def print_data(data):
    for i in range(0, len(data)):
        print(data[i])

def priori(c):
    slownik = {}
    unikat_klasy = []
    for i in c:
        if i[-1] not in unikat_klasy: unikat_klasy.append(i[-1])

    for x in unikat_klasy:
        temp_licznik = 0
        for y in range(0, len(c)):
            if c[y][-1] == x: temp_licznik += 1

        slownik[x] = temp_licznik / len(c)

    return slownik

def stats_by_class(c):
    slownik = {}
    unikat_klasy = []
    for i in c:
        if i[-1] not in unikat_klasy: unikat_klasy.append(i[-1])

    for klasa in unikat_klasy:
        obiekty_klasy = []
        for obiekt in c:
            if obiekt[-1] == klasa: obiekty_klasy.append(obiekt)

        statystyki = []
        for j in range(len(c[0]) - 1):
            kolumna = []
            for obiekt in obiekty_klasy:
                kolumna.append(obiekt[j])
            statystyki.append((np.mean(kolumna), np.var(kolumna)))

        slownik[klasa] = statystyki

    return slownik

def kross_walidacja(dane):
    kafelki = []
    obecne = []
    temp = []
    licznik = 0
    while(licznik != len(dane)):
        j = random.randint(0, 149)
        if j not in obecne:
            obecne.append(j)
            licznik = licznik + 1
            temp.append(dane[j])
            if len(temp) == 30:
                kafelki.append(temp)
                temp = []

    return kafelki

def macierz_pomylek(przewidzane, rzeczywiste, klasy):
    n = len(klasy)
    macierz = []
    for i in range(0, n):
        linia=[]
        for j in range(0,n):
            linia.append(0)
        macierz.append(linia)

    for i in range(len(rzeczywiste)):
        r = rzeczywiste[i]
        p = przewidzane[i]
        if r in klasy and p in klasy:
            macierz[klasy.index(p)][klasy.index(r)] += 1

    poprawne = sum(macierz[i][i] for i in range(n))
    accuracy = poprawne / len(rzeczywiste)

    print(f"macierz pomylek:")
    print(f"{"przewidziane \\ rzeczywiste":30}", end="")
    for k in klasy: print(f"{k:20}", end="")
    print("")
    for i in range(n):
        print(f"{klasy[i]:30}", end="")
        for j in range(n): print(f"{macierz[i][j]:<20}", end="")
        print("")
    print(f"accuracy: {accuracy}")

    return accuracy

def rozklad_normalny(war, atrybut, srednia):
    dol_ulamka = math.sqrt(2 * math.pi * war)
    do_potegi = -1 * ((atrybut - srednia) ** 2 / (2 * war))
    razem = 1 / dol_ulamka * math.e ** do_potegi
    return razem

def naive_bayes(tst, trn):
    procent_klas = priori(trn)
    stats = stats_by_class(trn)
    klasy = list(procent_klas.keys())
    przewidziane_klasy = []
    for obiekt in tst:
        wyniki = {}
        for klasa in klasy:
            log_suma = math.log(procent_klas[klasa])
            for j in range(len(obiekt) - 1):
                srednia, wariancja = stats[klasa][j]
                p_ai = rozklad_normalny(wariancja, obiekt[j], srednia)
                if p_ai > 0:
                    log_suma += math.log(p_ai)
                else:
                    log_suma += -9999999

            wyniki[klasa] = log_suma
        przewidziana = max(wyniki, key=wyniki.get)
        przewidziane_klasy.append(przewidziana)
    return przewidziane_klasy

def main():
    data = get_data("iris.data")
    kafelki = kross_walidacja(data)
    klasy = list(set(obiekt[-1] for obiekt in data))
    ogolne_accuracy = []

    for numer_kafla in range(5):
        print(f'\n---------------Iteracja {numer_kafla + 1}-------------------')

        zbior_testowy = kafelki[numer_kafla]
        zbior_treningowy = []

        for i in range(5):
            if i != numer_kafla:
                for obiekt in kafelki[i]:
                    zbior_treningowy.append(obiekt)

        rzeczywiste = [obiekt[-1] for obiekt in zbior_testowy]
        przewidziane = naive_bayes(zbior_testowy, zbior_treningowy)

        accuracy = macierz_pomylek(przewidziane, rzeczywiste, klasy)
        ogolne_accuracy.append(accuracy)

    srednia = sum(ogolne_accuracy) / len(ogolne_accuracy)
    print(f"\n---------------Srednie accuracy: {srednia}-------------------")

main()