from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit


app = Flask(__name__, template_folder="web")
socketio = SocketIO(app, async_handlers=True)  # Enable WebSocket support

counter = 0

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
    global counter
    command = request.form.get('command')
    
    if command == "left":
        print("left")
        counter -= 1
        socketio.emit('message', {'value': 'Recieved left','counter': str(counter), 'command': 'Left'})

    elif command == "right":
        print("right")
        counter += 1
        socketio.emit('message', {'value': 'Recieved right','counter': str(counter), 'command': 'Right'})        

    elif command == "stop":
        print("stop")
        socketio.emit('message', {'value': 'Recieved stop', 'command': 'Stop'})
    
    return "", 204  # No content response, just to acknowledge the request

if __name__ == "__main__":
    #app.run(host="0.0.0.0", port=8500)
    socketio.run(app, host="0.0.0.0", port=8500)
