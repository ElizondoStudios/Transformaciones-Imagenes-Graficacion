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

def interpolar(matriz):
    #Vamos a rellenar los pixeles que tengan la mayoría de sus pixeles en V4 encendidos
    interpolada= matriz
    for (i, row) in enumerate(matriz):
        for (j, pixel) in enumerate(row):
            vecino_arriba= matriz[i-1][j] if i>0 else 0
            vecino_abajo= matriz[i+1][j] if i<len(matriz)-1 else 0
            vecino_izquierda= matriz[i][j-1] if j>0 else 0
            vecino_derecho= matriz[i][j+1] if j<len(row)-1 else 0
            if pixel==0 and (vecino_arriba+vecino_abajo+vecino_izquierda+vecino_derecho)>765:
                interpolada[i][j]=255
    return interpolada

def rotacion(x, y, theta):
    coseno= cos(theta)
    seno= sin(theta)
    return (round(x*coseno+y*seno), round(y*coseno-x*seno))

def rotar_imagen(ruta, nombre_archivo, theta):
    img = Image.open(ruta)
    rgb_matriz= np.array(img)
    pixel_matriz= tuple(map(binarizar_row, rgb_matriz))
    
    #Rotar sobre el centro de masa del objeto
    filas= len(pixel_matriz)
    columnas= len(pixel_matriz)
    origen_x, origen_y= calcular_centros_masa(pixel_matriz)
    origen_x= round(origen_x)
    origen_y= round(origen_y)
    imagen_rotada= np.zeros((filas+100, columnas+100)) #Agregamos marcos de 50 pixeles

    for (i, row) in enumerate(pixel_matriz):
        for (j, pixel) in enumerate(row):
            if(pixel==1):
                i2, j2= rotacion(i-origen_x, j-origen_y, (theta/180)*pi) #Usar grados en lugar de pi radianes
                if (i2+origen_x)<columnas+50 and (j2+origen_y)<filas+50:
                    imagen_rotada[i2+origen_x+50][j2+origen_y+50]=255 #Ajustamos de coordenadas a pixeles en la imágen
    
    #Interpolamos la imágen para recuperar los pixeles perdidos al rotar
    imagen_interpolada= interpolar(imagen_rotada)
    
    #Guardar la imágen rotada e interpolada
    imagen_rotada_archivo= Image.fromarray(imagen_interpolada.astype(np.uint8))
    imagen_rotada_archivo.save(f"./Dataset_Rotado/{nombre_archivo}")