import cv2
import numpy as np
import sys

# Configuración de la ventana
WIDTH = 800
HEIGHT = 600
FPS = 30

# Dimensiones de cada sección
SECTION_WIDTH = WIDTH // 2
SECTION_HEIGHT = HEIGHT // 2

# Obtener la ruta del archivo de video en el directorio raíz del proyecto
video_file = "video.mp4"  # Ajusta el nombre del archivo de video si es necesario

# Cargar el video con OpenCV
cap = cv2.VideoCapture(video_file)

# Bucle principal del programa
while True:
    # Leer el siguiente fotograma del video
    ret, frame = cap.read()
    if not ret:
        break  # Si no hay más fotogramas, salir del bucle

    # Redimensionar el fotograma para que se ajuste a la ventana
    frame = cv2.resize(frame, (WIDTH, HEIGHT))

    # Dividir el fotograma en cuatro secciones
    sections = []

    # Secciones horizontales
    for y in range(2):
        section = frame[y * SECTION_HEIGHT:(y + 1) * SECTION_HEIGHT, :]
        sections.append(section)

    # Secciones verticales
    for x in range(2):
        section = frame[:, x * SECTION_WIDTH:(x + 1) * SECTION_WIDTH]
        sections.append(section)

    # Mostrar las secciones
    cv2.imshow("Section 1", sections[0])
    cv2.imshow("Section 2", sections[1])
    cv2.imshow("Section 3", sections[2])
    cv2.imshow("Section 4", sections[3])

    # Esperar el tiempo suficiente para mantener el FPS deseado
    if cv2.waitKey(int(1000 / FPS)) & 0xFF == ord('q'):
        break  # Si se presiona 'q', salir del bucle

# Liberar el objeto VideoCapture y cerrar las ventanas
cap.release()
cv2.destroyAllWindows()
