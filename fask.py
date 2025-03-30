<<<<<<< HEAD
from flask import Flask, render_template, request  
from flask_socketio import SocketIO, emit
import time
import threading
=======
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

import distance
>>>>>>> 2ba300acf2914ea429f92d82d918209a62bb93b2

app = Flask(__name__, template_folder="web")
socketio = SocketIO(app, async_handlers=True)  # Enable WebSocket support

counter = 0

def increment_counter():
    global counter
    while True:
        socketio.sleep(1)  # Non-blocking sleep that yields control back to the event loop
        counter += 1
        socketio.emit('update_counter', {'value': counter})

@socketio.on("my_event")
def poll():
    for x in range(5):
        distance_data = distance.get_distances()

        emit('server', {"distance1":1, "distance2":2}, room=sid)
        socketio.sleep(1)

@app.route('/')
def home():
   return render_template('index.html')
   
@socketio.on('connect')
def handle_connect():
    """Send the current counter value when the client connects."""
    socketio.emit('update_counter', {'value': counter})

@app.route('/control', methods=['POST'])
def control():
    global counter
    command = request.form.get('command')
    
    if command == "left":
        counter -= 1  # Decrement the counter
        print("left", counter)
        socketio.emit('update_counter', {'value': counter})  # Emit updated counter
    elif command == "right":
        counter += 1  # Increment the counter
        print("right", counter)
        socketio.emit('update_counter', {'value': counter})  # Emit updated counter
    elif command == "stop":
        print("stop")
    
    return "", 204  # No content response, just to acknowledge the request

"""
def update_text():
    global dynamic_text
    while True:
        new_text = input("Enter new text for the webpage: ")
        dynamic_text = new_text
"""

if __name__ == "__main__":
    #app.run(host="0.0.0.0", port=8500)
    socketio.run(app, host="0.0.0.0", port=8500)
