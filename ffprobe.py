import subprocess

# Comando para obtener el tiempo de reproducción actual del flujo UDP
command_get_time = [
    'ffprobe',
    '-v', 'error',
    '-show_entries', 'format=start_time',
    '-of', 'default=noprint_wrappers=1:nokey=1',
    'udp://192.168.100.115:12345'  # Asegúrate de reemplazar '192.168.100.115' con la IP correspondiente
]

# Ejecutar el comando para obtener el tiempo de reproducción actual
result = subprocess.run(command_get_time, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
start_time = float(result.stdout.decode().strip())

# Comando para reproducir el video recibido a través de UDP desde el tiempo actual
command_play = [
    'ffplay',
    '-i', 'udp://192.168.100.115:12345',
    '-ss', str(start_time)  # Iniciar la reproducción desde el tiempo actual
]

# Ejecutar el comando para iniciar la reproducción del video
subprocess.run(command_play)