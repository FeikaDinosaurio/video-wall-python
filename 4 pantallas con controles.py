import cv2
import numpy as np

# Configuración de la ventana
WIDTH = 1920
HEIGHT = 1080
FPS = 60

# Obtener la ruta del archivo de video en el directorio raíz del proyecto
video_file = "video.mp4"  # Ajusta el nombre del archivo de video si es necesario

# Cargar el video con OpenCV
cap = cv2.VideoCapture(video_file)

# Crear las ventanas
cv2.namedWindow("Section 1")
cv2.namedWindow("Section 2")
cv2.namedWindow("Section 3")
cv2.namedWindow("Section 4")

# Controles para cada pantalla
controls = {
    'a': {ord('8'): 'up', ord('2'): 'down', ord('6'): 'right', ord('4'): 'left', ord('1'): 'rotate_left',
          ord('3'): 'rotate_right', ord('5'): 'zoom_out', ord('7'): 'zoom_in'},
    'b': {ord('8'): 'up', ord('2'): 'down', ord('6'): 'right', ord('4'): 'left', ord('1'): 'rotate_left',
          ord('3'): 'rotate_right', ord('5'): 'zoom_out', ord('7'): 'zoom_in'},
    'c': {ord('8'): 'up', ord('2'): 'down', ord('6'): 'right', ord('4'): 'left', ord('1'): 'rotate_left',
          ord('3'): 'rotate_right', ord('5'): 'zoom_out', ord('7'): 'zoom_in'},
    'd': {ord('8'): 'up', ord('2'): 'down', ord('6'): 'right', ord('4'): 'left', ord('1'): 'rotate_left',
          ord('3'): 'rotate_right', ord('5'): 'zoom_out', ord('7'): 'zoom_in'}
}

# Posiciones iniciales
positions = [(0, 0), (0, 0), (0, 0), (0, 0)]

# Ángulo de rotación inicial
rotation_angles = {'a': 0, 'b': 0, 'c': 0, 'd': 0}
# Factor de escala inicial
scale_factors = {'a': 1.0, 'b': 1.0, 'c': 1.0, 'd': 1.0}

# Pantalla actual
current_screen = 'a'

# Bucle principal del programa
while True:
    # Leer el siguiente fotograma del video
    ret, frame = cap.read()
    if not ret:
        break  # Si no hay más fotogramas, salir del bucle

    # Redimensionar el fotograma para que se ajuste a la ventana
    frame = cv2.resize(frame, (WIDTH, HEIGHT))

    # Mostrar las secciones en ventanas separadas
    for i, screen in enumerate(['a', 'b', 'c', 'd']):
        # Obtener los controles para la pantalla actual
        current_controls = controls[screen]

        # Aplicar rotación al fotograma
        rotation_matrix = cv2.getRotationMatrix2D((frame.shape[1] // 2, frame.shape[0] // 2), rotation_angles[screen], scale_factors[screen])
        rotated_frame = cv2.warpAffine(frame, rotation_matrix, (frame.shape[1], frame.shape[0]))

        # Mover el fotograma en la dirección especificada
        x, y = positions[i]
        M = np.float32([[1, 0, x], [0, 1, y]])
        translated_frame = cv2.warpAffine(rotated_frame, M, (rotated_frame.shape[1], rotated_frame.shape[0]))

        # Mostrar la sección en la ventana correspondiente
        cv2.imshow(f"Section {i+1}", translated_frame)

    # Capturar la entrada del teclado
    key = cv2.waitKey(int(1000 / FPS)) & 0xFF

    # Cambiar la pantalla actual
    if key in [ord('a'), ord('b'), ord('c'), ord('d')]:
        current_screen = chr(key)


    # Control de teclado
    if key in controls[current_screen]:
        action = controls[current_screen][key]
        if action == 'up':
            positions[ord(current_screen) - ord('a')] = (positions[ord(current_screen) - ord('a')][0], positions[ord(current_screen) - ord('a')][1] - 10)
        elif action == 'down':
            positions[ord(current_screen) - ord('a')] = (positions[ord(current_screen) - ord('a')][0], positions[ord(current_screen) - ord('a')][1] + 10)
        elif action == 'left':
            positions[ord(current_screen) - ord('a')] = (positions[ord(current_screen) - ord('a')][0] - 10, positions[ord(current_screen) - ord('a')][1])
        elif action == 'right':
            positions[ord(current_screen) - ord('a')] = (positions[ord(current_screen) - ord('a')][0] + 10, positions[ord(current_screen) - ord('a')][1])
        elif action == 'rotate_left':
            rotation_angles[current_screen] -= 5
        elif action == 'rotate_right':
            rotation_angles[current_screen] += 5
        elif action == 'zoom_out':
            scale_factors[current_screen] -= 0.1
        elif action == 'zoom_in':
            scale_factors[current_screen] += 0.1

# Liberar el objeto VideoCapture y cerrar las ventanas
cap.release()
cv2.destroyAllWindows()
