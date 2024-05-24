import subprocess
import os
import time
from datetime import datetime
# Comando para reproducir el video recibido
# Hora de inicio en formato HH:MM:SS
start_time = "9:35:00"

while True:
    current_time = datetime.now().strftime("%H:%M:%S")
    if current_time == start_time:
        command = [
            'ffplay',
            '-i', 'udp://192.168.100.115:12345'  # Asegúrate de reemplazar '192.168.1.x' con la IP correspondiente
        ]
        subprocess.run(command)
        break
    time.sleep(0.1)
command = [
    'ffplay',
    '-i', 'udp://192.168.100.115:12345'  # Asegúrate de reemplazar '192.168.1.x' con la IP correspondiente
]

# Ejecutar el comando
subprocess.run(command)
