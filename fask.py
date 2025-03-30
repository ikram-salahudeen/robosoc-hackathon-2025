from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit


app = Flask(__name__, template_folder="web")
socketio = SocketIO(app, async_handlers=True)  # Enable WebSocket support


@app.route('/')
def home():
   return render_template('index.html')

# Friendly connect message
@socketio.on('connect')
def handle_connect():
    socketio.emit('message', {'value': 'Connected'})

# The html page sends this periodically to get some sensor data
@socketio.on("request_data")
def poll():
    # Gather data

    # Send it
    emit('data', {'test_number':842, 'duty':0.5, 'dir':'Left', 'distance': 3.333, 'slouch': 1.2})

# The HTML form sends this (works)
@app.route('/control', methods=['POST'])
def control():
    command = request.form.get('command')
    
    if command == "left":
        print("left")
        socketio.emit('message', {'value': 'Recieved left'})

    elif command == "right":
        print("right")
        socketio.emit('message', {'value': 'Recieved right'})

    elif command == "stop":
        print("stop")
        socketio.emit('message', {'value': 'Recieved stop'})
    
    return "", 204  # No content response, just to acknowledge the request

if __name__ == "__main__":
    #app.run(host="0.0.0.0", port=8500)
    socketio.run(app, host="0.0.0.0", port=8500)
