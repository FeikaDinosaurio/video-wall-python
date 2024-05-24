import socket
import cv2
import numpy as np

from fotogramas import descargar_video_en_ram


def recibir_comando_sincronizacion(sock):
    try:
        comando = sock.recv(4)
        return int.from_bytes(comando, byteorder='big')
    except Exception as e:
        print(f"Error al recibir el comando de sincronización: {e}")
        return None

def main():
    try:
        ruta_video = "publi.mp4"
        frames = descargar_video_en_ram(ruta_video)
        fps = 30

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 2**20)
        client_socket.connect(('192.168.100.115', 8000))
        print("Conexión establecida con el servidor.")

        while True:
            # Recibir comando de sincronización del servidor
            frame_index = recibir_comando_sincronizacion(client_socket)
            if frame_index is None:
                print("No se pudo recibir el comando de sincronización.")
                break

            # Mostrar el fotograma correspondiente localmente
            frame = frames[frame_index]
            cv2.imshow('Video', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except Exception as e:
        print(f"Error en la conexión o durante la recepción de datos: {e}")
    finally:
        client_socket.close()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
