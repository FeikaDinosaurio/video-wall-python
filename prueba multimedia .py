

import subprocess

# Lista de nombres de archivos de video
video_files = ["video1.mp4", "video2.mp4", "video3.mp4", "video4.mp4"]

# Iterar sobre la lista y abrir cada video en una nueva instancia del reproductor
for video_file in video_files:
    subprocess.Popen(['start', '', video_file], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
