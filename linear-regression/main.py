import matplotlib.pyplot as plt
import math

def get_data(name_of_file):
    result = []
    x = []
    y = []
    with open(name_of_file, "r") as f:
        for line in f:
            parts = line.split()
            x.append(float(parts[0]))
            y.append(float(parts[1]))

    result.append(x)
    result.append(y)
    return result

def calculate_srednia(data:list):
    acumulate = 0
    for i in data:
        acumulate += i

    return acumulate/len(data)

def calculate_odchylenie_standardowe(data:list,srednia_z_data):
    new_data = []
    acumulate = 0
    for i in data:
        new_data.append((i-srednia_z_data)**2)

    for i in new_data:
        acumulate += i

    return round(math.sqrt(acumulate/(len(data)-1)),2)

def korelacja_pearsona(data_x:list, data_y:list):
    if len(data_x) != len(data_y): return None

    acumulate_xy = 0
    acumulate_x = 0
    acumulate_y = 0
    for i in range(0, len(data_x)): acumulate_xy += data_x[i]*data_y[i]
    for i in range(0, len(data_x)): acumulate_x += data_x[i]
    for i in range(0, len(data_y)): acumulate_y += data_y[i]

    acumulate_x_potega = 0
    acumulate_y_potega = 0
    for i in range(0, len(data_x)): acumulate_x_potega += data_x[i]**2
    for i in range(0, len(data_x)): acumulate_y_potega += data_y[i]**2

    gora = len(data_x)*acumulate_xy-acumulate_x*acumulate_y
    dol = math.sqrt((len(data_x)*acumulate_x_potega-acumulate_x**2)*(len(data_y)*acumulate_y_potega-acumulate_y**2))
    result = gora/dol


    return round(result,2)

def main():
    data = get_data("data.txt")
    x = data[0]
    y = data[1]

    print(x)
    print(y)

    M_x = calculate_srednia(x)
    M_y = calculate_srednia(y)

    S_x = calculate_odchylenie_standardowe(x,M_x)
    S_y = calculate_odchylenie_standardowe(y,M_y)

    r = korelacja_pearsona(x,y)

    # print(M_x)
    # print(M_y)
    # print(S_x)
    # print(S_y)
    # print(r)

    if r > 0:
        print("korelacja dodatnia")
    elif r < 0:
        print("korelacja ujemna")
    else:
        print("korelacja nie występuje")
        return;

    b = (r * S_y)/S_x
    a = M_y - (b * M_x)
    b=round(b,2)
    a=round(a,2)
    # print(a)
    # print(b)

    print(f'Otrzymana funkcja liniowa: y={b}x{a}')

    zestaw = [0.0]

    while zestaw[-1] < x[-1]:
        nowa_wartosc = zestaw[-1] + 0.01
        zestaw.append(round(nowa_wartosc, 2))

    funkcja = [b * x + a for x in zestaw]

    plt.scatter(x, y, label='Wartości niezależne')
    plt.plot(zestaw, funkcja, label='Linia regresji')
    plt.title("funkcja")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.legend()

    plt.show()

    nowa_wartosc_X = float(input("Dodaj nowy element by przewidzieć następną wartosc dla X:"))
    nowa_wartosc_Y = b * nowa_wartosc_X + a
    x.append(nowa_wartosc_X)
    y.append(nowa_wartosc_Y)
    print(x)
    print(y)

main()