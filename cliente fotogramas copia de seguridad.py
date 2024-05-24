import socket
import cv2
import numpy as np

def recibir_fotograma(sock):
    frame_len = int.from_bytes(sock.recv(4), byteorder='big')
    frame_data = b''
    while len(frame_data) < frame_len:
        packet = sock.recv(frame_len - len(frame_data))
        if not packet:
            break
        frame_data += packet
    frame = np.frombuffer(frame_data, dtype=np.uint8)
    return cv2.imdecode(frame, cv2.IMREAD_COLOR)

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('192.168.100.113', 8000))
    print("Conexión establecida con el servidor.")

    while True:
        frame = recibir_fotograma(client_socket)
        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    client_socket.close()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()