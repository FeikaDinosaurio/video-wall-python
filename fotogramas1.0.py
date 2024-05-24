import cv2
import numpy as np
import time
import socket
from threading import Thread, Lock

def descargar_video_en_ram(ruta_video):
    """
    Carga un video en memoria RAM.
    Parámetros:
        ruta_video (str): Ruta del archivo de video.
    Retorna:
        lista: Una lista de matrices NumPy que representan los fotogramas del video.
    """
    video = cv2.VideoCapture(ruta_video)
    frames = []
    while True:
        ret, frame = video.read()
        if not ret:
            break
        frames.append(frame)
    video.release()
    return frames

def reproducir_video_local(frames, fps=60, global_frame_index=None, global_frame_index_lock=None):
    num_frames = len(frames)
    start_time = time.time()
    while True:
        with global_frame_index_lock:
            frame_index = global_frame_index[0]
        frame = frames[frame_index]
        cv2.imshow('Video', frame)
        elapsed_time = time.time() - start_time
        with global_frame_index_lock:
            global_frame_index[0] = int(elapsed_time * fps) % num_frames
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()

def enviar_fotogramas(client_socket, frames, fps=60, global_frame_index=None, global_frame_index_lock=None):
    num_frames = len(frames)
    start_time = time.time()
    while True:
        with global_frame_index_lock:
            frame_index = global_frame_index[0]
        frame = frames[frame_index]
        encoded_frame = cv2.imencode('.jpg', frame)[1].tobytes()
        try:
            client_socket.sendall(len(encoded_frame).to_bytes(4, byteorder='big'))
            client_socket.sendall(encoded_frame)
        except (ConnectionResetError, ConnectionAbortedError):
            print(f"El cliente {client_socket.getpeername()} ha cerrado la conexión.")
            break
        except OSError as e:
            if e.winerror == 10038:  # Error: se intentó realizar una operación en un elemento que no es un socket
                print(f"El socket del cliente {client_socket.getpeername()} ya está cerrado.")
            else:
                raise e

def handle_client(client_socket, frames, fps, global_frame_index, global_frame_index_lock):
    enviar_fotogramas(client_socket, frames, fps, global_frame_index, global_frame_index_lock)
    client_socket.close()
    print(f"Cliente desconectado: {client_socket.getpeername()}")

def main():
    ruta_video = "publi.mp4"
    frames = descargar_video_en_ram(ruta_video)
    fps = 30

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('192.168.100.115', 8000))
    server_socket.listen(5)
    print("Servidor iniciado. Esperando conexiones de clientes...")

    # Crear un objeto de bloqueo para acceder al índice de fofotograma global de manera segura
    global_frame_index_lock = Lock()

    # Crear un objeto de valor para el índice de fotograma global
    global_frame_index = np.array([0], dtype=np.uint32)

    # Iniciar hilo para la reproducción local del video
    local_video_thread = Thread(target=reproducir_video_local, args=(frames, fps, global_frame_index, global_frame_index_lock))
    local_video_thread.start()

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Nueva conexión establecida con {addr}")
        client_thread = Thread(target=handle_client, args=(client_socket, frames, fps, global_frame_index, global_frame_index_lock))
        client_thread.start()

    server_socket.close()

if __name__ == "__main__":
    main()