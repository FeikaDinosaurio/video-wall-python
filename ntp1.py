from flask import Flask, jsonify
from datetime import datetime, timezone

app = Flask(__name__)

# Define la hora de reproducción del video (ejemplo: 22 de mayo de 2024, 14:00:00 UTC)
video_play_time = datetime(2024, 5, 22, 14, 0, 0, tzinfo=timezone.utc)

@app.route('/time', methods=['GET'])
def get_time():
    # Devuelve la hora actual del servidor y la hora de reproducción del video
    now = datetime.now(timezone.utc)
    return jsonify({'current_time': now.isoformat(), 'video_play_time': video_play_time.isoformat()})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
