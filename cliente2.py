import os
import socket
import subprocess

# Ruta al ejecutable de FFmpeg
ffmpeg_path = r"C:\Users\supra\Documents\Programas\ffmpeg-master-latest-win64-gpl\ffmpeg-master-latest-win64-gpl\bin\ffmpeg.exe"
if os.path.exists("output.mp4"):
    os.remove("output.mp4")
# Dirección IP y puerto del servidor
SERVER_IP = '127.0.0.1'
SERVER_PORT = 5000

# Función para conectarse al servidor y recibir instrucciones
def connect_to_server():
    # Crear un socket TCP/IP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Conectar al servidor
        client_socket.connect((SERVER_IP, SERVER_PORT))

        # Recibir instrucciones del servidor
        instructions = client_socket.recv(1024).decode()
        print("Instrucciones del servidor:", instructions)

        # Comando para recortar y dividir el video usando FFmpeg
        command = [
            ffmpeg_path,
            "-i", "video.mp4",  # Archivo de entrada
            "-ss", "0",         # Tiempo de inicio (en segundos)
            "-t", "60",         # Duración del recorte (en segundos)
            "-an",              # Desactivar audio
            # Para la parte de arriba a la derecha
            "-vf", "crop=960:540:960:0",  # Recortar video
            "output.mp4"       # Archivo de salida
        ]

        # Ejecutar el comando usando subprocess
        subprocess.run(command)

    except ConnectionRefusedError:
        print("No se pudo conectar al servidor. Asegúrate de que el servidor esté en ejecución.")

    finally:
        # Cerrar el socket
        client_socket.close()


if __name__ == '__main__':
    connect_to_server()
