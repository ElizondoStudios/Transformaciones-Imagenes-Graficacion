from PIL import Image
import numpy as np
from math import *

threshold= 128

def binarizar_row(row):
    row_binario= []
    for pixel in row:
        row_binario.append(1 if int(np.mean(pixel))>threshold else 0)
    return row_binario

def crear_texto(matriz, nombre):
    try:
        f= open(nombre, "w")
        for row in matriz:
            f.write("".join("1" if pixel==1 else "0" for pixel in row))
            f.write("\n")
        f.close()
    except:
        print("Error al crear texto")
        pass

def procesar_imagen(ruta_img, ruta_txt):
    try:
        img = Image.open(ruta_img)
        rgb_matriz= np.array(img)
        pixel_matriz= tuple(map(binarizar_row, rgb_matriz))

        crear_texto(pixel_matriz, ruta_txt)
    except IOError:
        print("Unable to load image")
        pass


objetos= ["caballo", "campana", "elefante", "manzana", "murcielago", "pato", "perro", "pollo", "rana", "tortuga"]
for objeto in objetos:
    procesar_imagen(f"./Dataset/{objeto}.jpg", f"Dataset_Texto/{objeto}.txt")