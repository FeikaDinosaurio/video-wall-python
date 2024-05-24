import socket
import cv2
import numpy as np

# Configuración de la red
HOST = '192.168.100.115'  # Dirección IP de la PC maestra
PORT = 65432  # Puerto para la comunicación

# Ruta al archivo de video en la PC cliente
video_path = r"prueba.mp4"  # Ruta del archivo de video en la PC cliente

# Función para recibir los datos de la PC maestra
def receive_data():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        data = s.recv(1024 * 1024)  # Aumentar el tamaño del búfer
        if data:
            data = data.decode('utf-8')
            parts = data.split('|FRAME:')
            if len(parts) == 2:
                second = float(parts[0].split(':')[1])
                frame_bytes = parts[1].encode('utf-8')
                frame = np.frombuffer(frame_bytes, dtype=np.uint8)
                frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
                return second, frame
    return None, None

# Inicializar el objeto VideoCapture en la PC cliente
cap = cv2.VideoCapture(video_path)

# Bucle para recibir y ajustar la reproducción del video
while True:
    # Recibir el segundo de reproducción y el frame desde la PC maestra
    received_second, frame = receive_data()

    # Verificar si se recibieron datos válidos
    if received_second is None or frame is None:
        continue

    # Ajustar la posición del video según el segundo recibido
    current_position = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
    cap.set(cv2.CAP_PROP_POS_MSEC, received_second * 1000)

    # Mostrar el frame recibido
    cv2.imshow('Video', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar el objeto VideoCapture y cerrar la ventana
cap.release()
cv2.destroyAllWindows()
