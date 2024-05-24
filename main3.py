import socket

# Dirección IP y puerto del servidor
SERVER_IP = '127.0.0.1'
SERVER_PORT = 5000


# Función para enviar instrucciones a los clientes
def send_instructions_to_clients(instructions):
    # Crear un socket TCP/IP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Enlazar el socket a la dirección IP y al puerto del servidor
    server_socket.bind((SERVER_IP, SERVER_PORT))

    # Escuchar conexiones entrantes
    server_socket.listen()

    print("Esperando conexiones entrantes...")
    while True:
        # Aceptar la conexión entrante
        client_socket, client_address = server_socket.accept()

        try:
            # Enviar instrucciones al cliente
            client_socket.sendall(instructions.encode())
            print("Instrucciones enviadas a:", client_address)
        except:
            print("Error al enviar instrucciones al cliente:", client_address)

        # Cerrar la conexión con el cliente
        client_socket.close()


if __name__ == '__main__':
    # Instrucciones para el cliente (cambia esto según tus necesidades)
    instructions = "Reproducir video 'video.mp4' y dividirlo en secciones para el videowall"
    send_instructions_to_clients(instructions)
