import socket
import cv2
import time

def enviar_fotograma(sock, frame):
    try:
        _, buffer = cv2.imencode('.jpg', frame)
        frame_data = buffer.tobytes()
        frame_len = len(frame_data)
        sock.sendall(frame_len.to_bytes(4, byteorder='big') + frame_data)
    except Exception as e:
        print(f"Error al enviar el fotograma: {e}")

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 8000))
    server_socket.listen(1)
    print("Esperando conexiones...")
    conn, addr = server_socket.accept()
    print(f"Conexión aceptada de {addr}")

    cap = cv2.VideoCapture(0)  # Usa la cámara por defecto

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            enviar_fotograma(conn, frame)
            time.sleep(0.1)  # Agregar un pequeño retraso entre fotogramas para evitar saturación
    except Exception as e:
        print(f"Error en la transmisión: {e}")
    finally:
        cap.release()
        conn.close()
        server_socket.close()

if __name__ == "__main__":
    main()
