from flask import Flask, make_response, request
from flask_socketio import SocketIO, emit, send


# Initialization
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")


@app.route('/')
def index():
    return 'hi i\'m the index'


@socketio.on('connect')
def test_connect():
    print("Connected: " + request.namespace + "/" + request.sid)
    print(request.event)
    emit('connectevent', {'data': 'Connected', 'sid': request.sid})

@socketio.on('message')
def handle_message(message):
    print(request.values)
    print('received message: ' + message)
    send('ServerSend: ' + message)
    emit("message", "ServerEmit: "+message, broadcast=True)

@socketio.on('json', namespace='/living_room')
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    room = session.get('room')
    emit('message', {'msg': session.get('name') + ':' + message['msg']}, room=room)

@socketio.on('disconnect')
def handle_disconnect():
    print("Disconnected: " + request.namespace + "/" + request.sid)
    emit('connectevent', {'data': 'Disonnected', 'sid': request.sid}, broadcast=True)


if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=44444, debug=True, log_output=True)
