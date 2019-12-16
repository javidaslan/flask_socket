from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from pythonping import ping

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('ping event', namespace='/test')
def test_message(message):
    destination = message['data']
    response = ping(destination, count=5000)
    print(response)
    if all([response.success for response in response]):
        message = "success"
    elif not any([response.success for response in response]):
        message = "destination is not reachable"
    emit('ping response', {'data': message})

@socketio.on('my broadcast event', namespace='/test')
def test_message(message):
    emit('my response', {'data': 'sending from my broadcast'}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)