from flask import Flask, jsonify, request
from datetime import datetime, timezone
import threading
from datetime import datetime, timedelta, timezone

app = Flask(__name__)

# Variables globales
video_play_time = None
clients_connected = 0
clients_required = 1
condition = threading.Condition()

@app.route('/time', methods=['GET'])
def get_time():
    global clients_connected

    # Incrementa el conteo de clientes conectados
    with condition:
        clients_connected += 1
        if clients_connected >= clients_required:
            # Establece la hora de reproducción del video si no está establecida
            if video_play_time is None:
                set_video_play_time()
            # Notifica a todos los clientes que la reproducción puede comenzar
            condition.notify_all()

    # Espera hasta que se alcance el número requerido de clientes conectados
    with condition:
        while clients_connected < clients_required:
            condition.wait()

    # Devuelve la hora actual del servidor y la hora de reproducción del video
    now = datetime.now(timezone.utc)
    return jsonify({
        'current_time': now.isoformat(),
        'video_play_time': video_play_time.isoformat()
    })

def set_video_play_time():
    global video_play_time
    # Define la hora de reproducción del video (5 segundos en el futuro)
    video_play_time = datetime.now(timezone.utc) + timedelta(seconds=5)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
