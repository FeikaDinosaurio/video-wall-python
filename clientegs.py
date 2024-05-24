import cv2
import time
import tkinter as tk
from tkinter import ttk
import socket
from PIL import Image, ImageTk

class VideoPlayer:
    def __init__(self, video_source, canvas):
        self.video_source = video_source
        self.canvas = canvas
        self.cap = cv2.VideoCapture(self.video_source)
        self.start_time = time.time()

    def draw_video(self):
        ret, frame = self.cap.read()
        if ret:
            self.canvas.delete("all")
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.tk_img = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.tk_img, anchor=tk.NW)
            self.canvas.after(10, self.draw_video)
        else:
            print("Error al leer el video")

def main():
    root = tk.Tk()
    root.title("Videowall Multidispositivos")

    width = 1920
    height = 1080
    canvas = tk.Canvas(root, width=width, height=height)
    canvas.pack()

    video_path = r"C:\Users\supra\PycharmProjects\pythonvideowall\publicidad.mp4"  # Ruta del video
    video_player = VideoPlayer(video_path, canvas)

    # Crear un socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Conectarse al servidor
    server_address = ('192.168.100.113', 1234)
    client_socket.connect(server_address)

    print("Conectado al servidor. Esperando orden de reproducir...")

    while True:
        # Recibir la orden de reproducir del servidor
        data = client_socket.recv(1024)
        if data == b"play":
            print("Orden de reproducir recibida. Reproduciendo video...")
            video_player.draw_video()
            break

    root.mainloop()

if __name__ == "__main__":
    main()