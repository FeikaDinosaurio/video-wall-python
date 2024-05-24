import cv2
import numpy as np
import time
import socket
from threading import Thread, Lock


def leer_fotograma(video, frame_index):
    video.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
    ret, frame = video.read()
    if not ret:
        return None
    return frame


def reproducir_video_local(ruta_video, fps=30, global_frame_index=None, global_frame_index_lock=None):
    video = cv2.VideoCapture(ruta_video)
    num_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    start_time = time.time()
    while True:
        with global_frame_index_lock:
            frame_index = global_frame_index[0]
        frame = leer_fotograma(video, frame_index)
        if frame is None:
            break
        cv2.imshow('Video', frame)
        elapsed_time = time.time() - start_time
        with global_frame_index_lock:
            global_frame_index[0] = int(elapsed_time * fps) % num_frames
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    video.release()
    cv2.destroyAllWindows()


def enviar_fotogramas(client_socket, ruta_video, fps=45, global_frame_index=None, global_frame_index_lock=None):
    video = cv2.VideoCapture(ruta_video)
    num_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    start_time = time.time()
    while True:
        with global_frame_index_lock:
            frame_index = global_frame_index[0]
        frame = leer_fotograma(video, frame_index)
        if frame is None:
            break

        # Mejora la calidad de la compresión JPEG
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 120]
        encoded_frame = cv2.imencode('.jpg', frame, encode_param)[1].tobytes()

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
        time.sleep(1 / fps)
    video.release()


def handle_client(client_socket, ruta_video, fps, global_frame_index, global_frame_index_lock):
    enviar_fotogramas(client_socket, ruta_video, fps, global_frame_index, global_frame_index_lock)
    client_socket.close()
    print(f"Cliente desconectado: {client_socket.getpeername()}")


def main():
    ruta_video = "publi.mp4"
    fps = 60

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('192.168.100.115', 8000))
    server_socket.listen(5)
    print("Servidor iniciado. Esperando conexiones de clientes...")

    global_frame_index_lock = Lock()
    global_frame_index = np.array([0], dtype=np.uint32)

    local_video_thread = Thread(target=reproducir_video_local,
                                args=(ruta_video, fps, global_frame_index, global_frame_index_lock))
    local_video_thread.start()

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Nueva conexión establecida con {addr}")
        client_thread = Thread(target=handle_client,
                               args=(client_socket, ruta_video, fps, global_frame_index, global_frame_index_lock))
        client_thread.start()

    server_socket.close()


if __name__ == "__main__":
    main()
