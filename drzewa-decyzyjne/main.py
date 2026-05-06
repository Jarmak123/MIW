import math
import numpy as np

def get_data(input):
    data = []
    with open(input, 'r') as f:
        for line in f:
            data.append(line.split())
    return data

def print_data(data):
    for row in data:
        print(row)

def entropia(data, klucz):
    negatywy=0
    pozytywy=0
    zapisz_index=0
    for i in range(0,data[0]):
        if data[0][i]==klucz: zapisz_index=i

    for i in range(1,len(data)):
        pass



def main():
    data = get_data("data.txt")
    print_data(data)

main()