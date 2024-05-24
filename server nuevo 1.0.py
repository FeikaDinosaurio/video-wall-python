import socket
import threading
import cv2

# Dirección y puerto del servidor
SERVER_ADDRESS = "192.168.100.115"
SERVER_PORT = 5050

# Ruta al video local
VIDEO_PATH = "publi.mp4"

# Número de clientes que deben estar listos para reproducir
NUM_CLIENTS_READY = 4

# Lock para la variable compartida num_clients_ready
lock = threading.Lock()
num_clients_ready = 0

def handle_client(conn, addr):
    global num_clients_ready

    print(f"[NEW CONNECTION] {addr} connected.")

    while True:
        msg = conn.recv(1024).decode()
        if msg == "cliente listo para reproducir":
            with lock:
                num_clients_ready += 1
                print(f"[CLIENT READY] {addr} is ready to play video.")
                if num_clients_ready == NUM_CLIENTS_READY:
                    print("[SERVER] All clients ready, sending play command.")
                    play_video()
        elif not msg:
            break

    conn.close()

def play_video():
    cap = cv2.VideoCapture(VIDEO_PATH)
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            cv2.imshow('Video', frame)
            if cv2.waitKey(30) & 0xFF == ord('q'):
                break
        else:
            break
    cap.release()
    cv2.destroyAllWindows()

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
