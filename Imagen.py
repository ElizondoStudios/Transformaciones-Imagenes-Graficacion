from PIL import Image
import numpy as np
from math import *

threshold = 128


def binarizar_row(row):
    row_binario = []
    for pixel in row:
        row_binario.append(1 if int(np.mean(pixel)) > threshold else 0)
    return row_binario


def crear_texto(matriz, nombre):
    try:
        f = open(nombre, "w")
        for row in matriz:
            f.write("".join("1" if pixel == 1 else "0" for pixel in row))
            f.write("\n")
        f.close()
    except:
        print("Error al crear texto")
        pass


def contar_pixeles(matriz):
    cuenta = 0
    for row in matriz:
        for pixel in row:
            if pixel == 1:
                cuenta += 1
    return cuenta


def calcular_centros_masa(matriz):
    sum_x = 0
    sum_y = 0
    N = 0
    for i in range(len(matriz)):
        row = matriz[i]
        for j in (range(len(row))):
            pixel = row[j]
            if (pixel == 1):
                N += 1
                sum_x += i
                sum_y += j
    return (sum_x / N, sum_y / N)

# Invariantes


def calcular_miu(matriz, p, q):
    centro_masa_x, centro_masa_y = calcular_centros_masa(matriz)
    miu = 0
    for i in range(len(matriz)):
        row = matriz[i]
        for j in (range(len(row))):
            pixel = row[j]
            if (pixel == 1):
                miu += pow((i - centro_masa_x), p) * pow((j - centro_masa_y), q)
    return miu


def calcular_eta(matriz, p, q):
    eta = calcular_miu(matriz, p, q) / pow((calcular_miu(matriz, 0, 0)), (((p + q) / 2) + 1))
    return eta


def calcular_phi_1(matriz):
    return calcular_miu(matriz, 2, 0) + calcular_miu(matriz, 0, 2)


def calcular_phi_2(matriz):
    return pow((calcular_miu(matriz, 2, 0) - calcular_miu(matriz, 0, 2)), 2) + 4 * (pow(calcular_miu(matriz, 1, 1), 2))


def calcular_phi_3(matriz):
    return pow((calcular_miu(matriz, 3, 0) - (3 * calcular_miu(matriz, 1, 2))), 2) + pow(((3 * calcular_miu(matriz, 2, 1)) - calcular_miu(matriz, 0, 3)), 2)


def calcular_contorno(matriz: np.ndarray[np.int8]) -> Image:
    if not isinstance(matriz, np.ndarray):
        matriz = np.array(matriz)

    eroded = np.zeros_like(matriz)

    for x in range(0, len(matriz) - 1):
        for y in range(0, len(matriz[0]) - 1):
            if matriz[x][y] == 1:
                sub_matriz = matriz[x - 1:x + 2, y - 1:y + 2]
                if np.sum(sub_matriz) == 9:
                    eroded[x][y] = 1

    # Al relleno lo pasamos a negativo de esta forma
    eroded *= -1
    # Como el relleno es -1 y el original es 1, sumamos los dos
    # al sumar los dos, esto hace que el relleno que seria 1 se convierta en 0 (1 - 1)
    # y el contorno seria (1 - 0)
    matriz += eroded

    return Image.fromarray((matriz * 255).astype(np.uint8))


def info_imagen(ruta):
    try:
        img = Image.open(ruta)
        rgb_matriz = np.array(img)
        pixel_matriz = tuple(map(binarizar_row, rgb_matriz))

        centro_masa = calcular_centros_masa(pixel_matriz)
        pixeles = contar_pixeles(pixel_matriz)

        return {
            "pixeles": pixeles,
            "centro_masa_x": centro_masa[0],
            "centro_masa_y": centro_masa[1],
            "miu_00": round(calcular_miu(pixel_matriz, 0, 0), 5),
            "miu_11": round(calcular_miu(pixel_matriz, 1, 1), 5),
            "miu_22": round(calcular_miu(pixel_matriz, 2, 2), 5),
            "eta_00": round(calcular_eta(pixel_matriz, 0, 0), 5),
            "eta_11": round(calcular_eta(pixel_matriz, 1, 1), 5),
            "eta_22": round(calcular_eta(pixel_matriz, 2, 2), 5),
            "phi_1": round(calcular_phi_1(pixel_matriz), 5),
            "phi_2": round(calcular_phi_2(pixel_matriz), 5),
            "phi_3": round(calcular_phi_3(pixel_matriz), 5)
        }
    except IOError:
        print("Unable to load image")
        pass
