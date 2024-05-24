import socket
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import imageio
import threading
import ntplib
from time import time, sleep

# Configuración del servidor
SERVER_IP = '192.168.100.113'  # IP del servidor
SERVER_PORT = 12345


def get_ntp_time(retries=3):
    ntp_client = ntplib.NTPClient()
    servers = ['pool.ntp.org', 'time.google.com', 'time.windows.com', 'time.nist.gov']
    for _ in range(retries):
        for server in servers:
            try:
                response = ntp_client.request(server, version=3)
                latency = (response.dest_time - response.orig_time) / 2
                return response.tx_time, latency
            except Exception as e:
                print(f"Error al obtener la hora de {server}: {e}")
        sleep(1)
    raise Exception("No se pudo obtener la hora de ningún servidor NTP.")


def play_video():
    def stream(label):
        video_path = r"C:\Users\supra\PycharmProjects\pythonvideowall\publicidad.mp4"
        video = imageio.get_reader(video_path)
        for image in video.iter_data():
            frame_image = ImageTk.PhotoImage(Image.fromarray(image))
            label.config(image=frame_image)
            label.image = frame_image
            label.update()

    video_window = tk.Tk()

