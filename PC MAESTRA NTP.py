def enviar_comandos_sincronizacion(client_socket, frames, fps=30, global_frame_index=None, global_frame_index_lock=None):
    num_frames = len(frames)
    start_time = time.time()
    while True:
        with global_frame_index_lock:
            frame_index = global_frame_index[0]
        elapsed_time = time.time() - start_time
        frame_index = int(elapsed_time * fps) % num_frames
        try:
            client_socket.sendall(frame_index.to_bytes(4, byteorder='big'))
            time.sleep(1 / fps)  # Esperar el tiempo correspondiente al FPS
        except (ConnectionResetError, ConnectionAbortedError):
            print(f"El cliente {client_socket.getpeername()} ha cerrado la conexión.")
            break
        except OSError as e:
            if e.winerror == 10038:  # Error: se intentó realizar una operación en un elemento que no es un socket
                print(f"El socket del cliente {client_socket.getpeername()} ya está cerrado.")
            else:
                raise e