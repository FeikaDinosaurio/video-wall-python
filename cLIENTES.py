import socket
import cv2
import time

# Configuración de la red
HOST = '192.168.100.115'  # Cambia esto por la dirección IP de la PC maestra
PORT = 65432  # Puerto para la comunicación

# Ruta al archivo de video en la PC cliente
video_path = r"C:\\Users\\supra\\PycharmProjects\\pythonvideowall\\prueba.mp4"

# Función para recibir el segundo de reproducción de la PC maestra
def receive_second():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        data = s.recv(1024)  # Esperar el segundo de reproducción
        return float(data.decode('utf-8').split(':')[1])

# Inicializar el objeto VideoCapture en la PC cliente
cap = cv2.VideoCapture(video_path)

# Inicializar el temporizador
last_adjustment_time = time.time()

# Bucle para recibir y ajustar la reproducción del video
while True:
    # Ajusta la reproducción del video en la PC cliente según el segundo recibido
    received_second = receive_second()
    current_second = received_second + 2  # Agregar 2 segundos al tiempo recibido
    current_position = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000

    # Ajustar la posición del video solo si el nuevo tiempo es mayor
    if current_second > current_position:
        cap.set(cv2.CAP_PROP_POS_MSEC, current_second * 1000)
        last_adjustment_time = time.time()  # Reiniciar el temporizador

    # Reproducir el video de forma continua
    while True:
        # Lee el siguiente frame del video
        ret, frame = cap.read()

        # Muestra el frame en la ventana
        if ret:
            cv2.imshow('Video', frame)

            # Salir del bucle si se presiona la tecla 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break

        # Ajustar la posición del video cada 15 segundos
        if time.time() - last_adjustment_time >= 15:
            break

# Liberar el objeto VideoCapture y cerrar la ventana
cap.release()
cv2.destroyAllWindows()