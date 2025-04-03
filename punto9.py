import numpy as np
import matplotlib.pyplot as plt
from skimage import morphology



# Ruta del archivo (reemplaza con la ruta de tu imagen)
file_path = "Transformaciones-Imagenes-Graficacion/Dataset_Texto/tortuga.txt"
save_path = "Transformaciones-Imagenes-Graficacion/Imagenes_SN_Ruido/tortuga_ruido.png"

# Leer el archivo asegurando que los valores sean enteros
with open(file_path, "r") as f:
    binary_image = np.array([list(line.strip()) for line in f], dtype=int)

# Definir el elemento estructurante
selem = morphology.disk(10)

# Aplicar operadores morfológicos
image_opened = morphology.opening(binary_image, selem)
image_closed = morphology.closing(binary_image, selem)
image_smooth_outer = morphology.closing(morphology.opening(binary_image, selem), selem)
image_smooth_inner = morphology.opening(morphology.closing(binary_image, selem), selem)
image_skeleton = morphology.skeletonize(binary_image)

# Mostrar los resultados
plt.figure(figsize=(12, 12))
plt.title("disk(10)\n")
plt.axis("off")

plt.subplot(2, 3, 1)
plt.imshow(binary_image, cmap="gray")
plt.title("Original")
plt.axis("off")

plt.subplot(2, 3, 2)
plt.imshow(image_opened, cmap="gray")
plt.title("Elimina regiones blancas en fondo negro", fontsize=8)
plt.axis("off")

plt.subplot(2, 3, 3)
plt.imshow(image_closed, cmap="gray")
plt.title(" Elimina agujeros negros en regiones blancas", fontsize=8)
plt.axis("off")

plt.subplot(2, 3, 4)
plt.imshow(image_smooth_outer, cmap="gray")
plt.title("Suavizar bordes exteriores")
plt.axis("off")

plt.subplot(2, 3, 5)
plt.imshow(image_smooth_inner, cmap="gray")
plt.title("Suavizar bordes interiores")
plt.axis("off")

plt.subplot(2, 3, 6)
plt.imshow(image_skeleton, cmap="gray")
plt.title("Esqueleto")
plt.axis("off")

plt.savefig(save_path)
plt.show()