import requests
import time
import cv2 # Importar OpenCV para la reproducción de video
from datetime import datetime, timedelta, timezone

def get_server_time(server_url):
    response = requests.get(f"{server_url}/time")
    data = response.json()
    server_time = datetime.fromisoformat(data['current_time']).replace(tzinfo=timezone.utc)
    video_play_time = datetime.fromisoformat(data['video_play_time']).replace(tzinfo=timezone.utc)
    video_pause_time_offset = data['video_pause_time_offset']
    return server_time, video_play_time, video_pause_time_offset

def synchronize_time(server_url):
    server_time, video_play_time, video_pause_time_offset = get_server_time(server_url)
    local_time = datetime.now(timezone.utc)
    offset = (server_time - local_time).total_seconds()
    return offset, video_play_time, video_pause_time_offset

def wait_until(target_time, offset):
    current_time = datetime.now(timezone.utc) + timedelta(seconds=offset)
    while current_time < target_time:
        time.sleep((target_time - current_time).total_seconds())
        current_time = datetime.now(timezone.utc) + timedelta(seconds=offset)

def play_video(video_path, video_pause_time_offset, offset):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: No se pudo abrir el video.")
        return

    video_start_time = datetime.now(timezone.utc) + timedelta(seconds=offset)
    pause_time = video_start_time + timedelta(seconds=video_pause_time_offset)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow('Video', frame)

        # Pausa el video en el tiempo indicado por pause_time
        current_time = datetime.now(timezone.utc)
        if current_time >= pause_time:
            cv2.waitKey()
            break

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    server_url = "http://192.168.100.115:5000" # Reemplaza con la URL correcta del servidor
    video_path = r"C:\Users\supra\PycharmProjects\pythonvideowall\publi.mp4" # Reemplaza con la ruta real de tu video
    offset, video_play_time, video_pause_time_offset = synchronize_time(server_url)
    wait_until(video_play_time, offset)
    play_video(video_path, video_pause_time_offset, offset)