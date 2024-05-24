import socket
import cv2
import time
import threading

# Configuración de la red
HOST = '192.168.100.115'  # Cambia esto por la dirección IP de la PC maestra
PORT = 65432  # Puerto para la comunicación
NUM_CLIENTS = 3  # Número de PCs clientes

# Ruta al archivo de video
video_path = r"C:\\Users\\supra\\PycharmProjects\\pythonvideowall\\prueba.mp4"

# Inicializar el objeto VideoCapture
cap = cv2.VideoCapture(video_path)

# Comprobar si la apertura del video fue exitosa
if not cap.isOpened():
    print("Error al abrir el video")
    exit()

# Función para reproducir el video
def play_video():
    while cap.isOpened():
        ret, frame = cap.read()  # Leer el siguiente frame del video
        if ret:
            cv2.imshow('Video', frame)  # Mostrar el frame
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
    cap.release()
    cv2.destroyAllWindows()

# Función para enviar los datos a través del socket
def send_data():
    while cap.isOpened():
        current_second = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000  # Obtener el segundo actual de reproducción del video
        if int(current_second) % 1 == 0:  # Enviar cada segundo
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((HOST, PORT))
                s.listen()
                for _ in range(NUM_CLIENTS):
                    conn, addr = s.accept()
                    with conn:
                        conn.sendall(f'SECOND:{current_second}'.encode('utf-8'))
        time.sleep(0.1)  # Agregar un retraso de 0.1 segundos entre cada iteración del bucle

# Crear hilos para la reproducción del video y el envío de datos
video_thread = threading.Thread(target=play_video)
send_data_thread = threading.Thread(target=send_data)

# Iniciar los hilos
video_thread.start()
send_data_thread.start()

# Esperar a que los hilos terminen
video_thread.join()
send_data_thread.join()