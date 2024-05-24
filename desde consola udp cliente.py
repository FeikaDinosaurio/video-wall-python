import time
from datetime import datetime
import subprocess

# Hora de inicio en formato HH:MM:SS
start_time = "09:47:00"

# Función para esperar hasta la hora especificada
def wait_until(start_time):
    while True:
        current_time = datetime.now().strftime("%H:%M:%S")
        if current_time == start_time:
            break
        time.sleep(0.1)

# Esperar hasta la hora especificada
wait_until(start_time)

# Comando para reproducir el video recibido a través de UDP
command = [
    'ffplay',
    '-i', 'udp://192.168.100.115:12345'  # Asegúrate de reemplazar '192.168.100.115' con la IP correspondiente
]

# Ejecutar el comando para iniciar la reproducción del video
subprocess.run(command)
