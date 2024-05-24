from flask import Flask, send_from_directory

app = Flask(__name__)


@app.route('/')
def index():
    return 'Servidor de videos en Flask'


@app.route('/video')
def video():
    return send_from_directory('.', 'video.mp4')


if __name__ == '__main__':
    app.run(debug=True)
