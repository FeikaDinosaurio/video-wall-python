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
last_received_second = 0

# Bucle para recibir y ajustar la reproducción del video
while True:
    # Ajustar la reproducción del video en la PC cliente según el segundo recibido
    current_time = time.time()
    if current_time - last_adjustment_time >= 1:  # Ajustar cada segundo
        current_position = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000

        # Ajustar la posición del video solo si es necesario
        if last_received_second > current_position:
            cap.set(cv2.CAP_PROP_POS_MSEC, last_received_second * 1000)

        last_adjustment_time = current_time  # Reiniciar el temporizador

    # Recibir el segundo de reproducción de la PC maestra
    received_second = receive_second()
    if received_second > last_received_second:
        last_received_second = received_second

    # Leer y mostrar el siguiente frame del video
    ret, frame = cap.read()
    if ret:
        cv2.imshow('Video', frame)

        # Salir del bucle si se presiona la tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# Liberar el objeto VideoCapture y cerrar la ventana
cap.release()
cv2.destroyAllWindows()
