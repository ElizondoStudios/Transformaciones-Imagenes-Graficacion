import numpy as np
import matplotlib.pyplot as plt
import os

# Ruta del archivo
file_path = "Transformaciones-Imagenes-Graficacion/Dataset_Texto/tortuga.txt"

# Leer el archivo asegurando que los valores sean enteros
with open(file_path, "r") as f:
    binary_matrix = np.array([list(line.strip()) for line in f], dtype=int)

# Crear la figura y mostrar la imagen
fig, ax = plt.subplots(figsize=(8, 8))
ax.imshow(binary_matrix, cmap="gray_r")  # Mostrar la imagen

# Dibujar la cuadrícula sobre la imagen
rows, cols = binary_matrix.shape
ax.set_xticks(np.arange(-0.5, cols, 1), minor=True)
ax.set_yticks(np.arange(-0.5, rows, 1), minor=True)
ax.grid(which="minor", color="gray", linestyle="-", linewidth=0.5)

# Ocultar etiquetas de los ejes
ax.set_xticklabels([])
ax.set_yticklabels([])

# Ruta para guardar la imagen (ajusta la carpeta según sea necesario)
save_path = "Transformaciones-Imagenes-Graficacion/Graficos_Computadora_Celdas/tortuga_cuadricula.png"

# Asegurarse de que el directorio exista
os.makedirs(os.path.dirname(save_path), exist_ok=True)

# Guardar la imagen
plt.savefig(save_path)

# Mostrar la imagen (opcional)
#plt.show()