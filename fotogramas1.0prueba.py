import cv2
import numpy as np
import time
import socket
from threading import Thread

def leer_siguiente_fotograma(video_capture):
    ret, frame = video_capture.read()
    if ret:
        return frame
    else:
        return None

def enviar_fotogramas(client_socket, video_capture, fps=30):
    start_time = time.time()
    while True:
        frame = leer_siguiente_fotograma(video_capture)
        if frame is None:
            break
        encoded_frame = cv2.imencode('.jpg', frame)[1].tobytes()
        try:
            client_socket.sendall(len(encoded_frame).to_bytes(4, byteorder='big'))
            client_socket.sendall(encoded_frame)
        except (ConnectionResetError, ConnectionAbortedError):
            print(f"El cliente {client_socket.getpeername()} ha cerrado la conexión.")
            break
        except OSError as e:
            if e.winerror == 10038:
                print(f"El socket del cliente {client_socket.getpeername()} ya está cerrado.")
            else:
                raise e

def handle_client(client_socket, video_capture, fps):
    try:
        enviar_fotogramas(client_socket, video_capture, fps)
    finally:
        client_socket.close()
        print(f"Cliente desconectado: {client_socket.getpeername()}")

def main():
    ruta_video = "publi.mp4"
    video_capture = cv2.VideoCapture(ruta_video)
    fps = 30

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('192.168.100.113', 8000))
    server_socket.listen(5)
    print("Servidor iniciado. Esperando conexiones de clientes...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Nueva conexión establecida con {addr}")
        client_thread = Thread(target=handle_client, args=(client_socket, video_capture, fps))
        client_thread.start()

if __name__ == "__main__":
    main()
