import subprocess

# Comando para transmitir el video
command = [
    'ffmpeg',
    '-re',
    '-i', r'C:\Users\supra\PycharmProjects\pythonvideowall\publi.mp4',
    '-f', 'mpegts',
    'udp://192.168.100.115:12345'
]

# Ejecutar el comando en segundo plano
process = subprocess.Popen(command)

# Mantener el script activo para que el proceso no se cierre
try:
    print("Transmitting video...")
    process.wait()  # Espera a que el proceso termine (aunque no debería)
except KeyboardInterrupt:
    process.terminate()  # Permite terminar el proceso con Ctrl+C
    print("Transmission terminated.")
