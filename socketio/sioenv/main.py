from flask import Flask, make_response, request
from flask_socketio import SocketIO, emit, send
from flask_socketio import join_room, leave_room


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
    send('ServerSend: ' + message, to="testroom")
    emit("message", "ServerEmit: "+message, broadcast=True)


@socketio.on('join')
def on_join():
    room = "testroom"
    join_room(room)
    send(request.sid + ' has entered the room.', to=room)

@socketio.on('leave')
def on_leave(data):
    room = 'testroom'
    leave_room(room)
    send(data['msg'] + ' has left the room.', to=room)

@socketio.on('json', namespace='/my_namespace')
def text(message):
    emit('message', "Namespace Message from " + request.sid, broadcast=True)
    print("namespace json")

@socketio.on('disconnect')
def handle_disconnect():
    print("Disconnected: " + request.namespace + "/" + request.sid)
    emit('connectevent', {'data': 'Disonnected', 'sid': request.sid}, broadcast=True)


if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=44444, debug=True, log_output=True)
