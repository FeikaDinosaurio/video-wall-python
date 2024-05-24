import requests
import shutil
import os
from moviepy.editor import VideoFileClip

# Descargar el video desde el servidor
server_url = 'http://localhost:5000/video'
response = requests.get(server_url, stream=True)

if response.status_code == 200:
    with open('video.mp4', 'wb') as f:
        response.raw.decode_content = True
        shutil.copyfileobj(response.raw, f)

# Reproducir el video
clip = VideoFileClip('video.mp4')
clip.preview()
clip.close()

# Eliminar el video después de reproducirlo
os.remove('video.mp4')

