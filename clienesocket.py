# Script para las PCs clientes

import socket
import cv2

# Configuración de la red
HOST = 'dirección_IP_de_la_PC_maestra'  # Cambia esto por la dirección IP de la PC maestra
PORT = 65432  # Puerto para la comunicación

# Ruta al archivo de video en cada PC cliente
video_path = 'ruta/al/video.mp4'

# Inicializar el objeto VideoCapture
cap = cv2.VideoCapture(video_path)

# Comprobar si la apertura del video fue exitosa
if not cap.isOpened():
    print("Error al abrir el video")

# Crear socket y conectar a la PC maestra
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    data = s.recv(1024)  # Esperar señal de inicio

    # Bucle de reproducción del video
    while cap.isOpened():
        ret, frame = cap.read()

        if ret:
            # Mostrar el frame
            cv2.imshow('Video', frame)

            # Esperar 25ms y salir si se presiona la tecla 'q'
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        else:
            break

# Liberar el objeto VideoCapture y cerrar la ventana
cap.release()
cv2.destroyAllWindows()
