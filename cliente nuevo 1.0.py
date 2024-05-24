import socket
import cv2
import numpy as np
import threading

# Dirección y puerto del servidor
SERVER_ADDRESS = "192.168.100.115"
SERVER_PORT = 5050

# Ruta al video local
VIDEO_PATH = "publi.mp4"

# Variable compartida para controlar la reproducción
play_video_event = threading.Event()

def load_video_to_memory():
    # Cargar el video a la RAM
    cap = cv2.VideoCapture(VIDEO_PATH)
    frames = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
    cap.release()
    return frames

def client_receive_order(conn):
    while True:
        msg = conn.recv(1024).decode()
        if msg == "play":
            play_video_event.set()
        elif not msg:
            break

def play_video_from_memory(frames, conn):
    for frame in frames:
        cv2.imshow('Video', frame)
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()
    conn.send("cliente listo para reproducir".encode())

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    frames = load_video_to_memory()
    thread_receive_order = threading.Thread(target=client_receive_order, args=(conn,))
    thread_receive_order.start()
    play_video_event.wait()
    play_video_from_memory(frames, conn)
    conn.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((SERVER_ADDRESS, SERVER_PORT))
    server.listen()

    print(f"[LISTENING] Server is listening on {SERVER_ADDRESS}:{SERVER_PORT}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

start_server()
