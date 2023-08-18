from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/caller')
def caller():
    return render_template('caller.html')

@app.route('/receiver')
def receiver():
    return render_template('receiver.html')

@socketio.on('signal')
def handle_signal(data):
    emit('signal', data, broadcast=True, include_self=False)

if __name__ == '__main__':
    socketio.run(app, debug=True)
