import subprocess

# Comando para reproducir el video recibido a través de UDP
command_play = [
    'ffplay',
    '-i', 'udp://192.168.100.115:12345'
]

# Ejecutar el comando para iniciar la reproducción del video
subprocess.run(command_play)
