from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import base64
import numpy as np
import io
import os
import motors
import sensor

app = Flask(__name__, template_folder="web")
socketio = SocketIO(app, async_handlers=True)  # Enable WebSocket support
duty = 0.5
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
    emit('data', {'test_number':842, 'duty':0.5, 'dir':'Left', 'distance1': sensor.get_distance1(), 'distance2': sensor.get_distance2(), 'slouch': 1.2})
    image_base64 = encode_image_from_file()
    if image_base64:
        socketio.emit('image_update', {'image': image_base64})
    detections = read_detections_from_file()
    socketio.emit('detections', {
            'detections': detections  # Send the detections with objects and scores
    })

@socketio.on("set_duty")
def set_duty(arg):
    global duty
    duty = float(arg)
    print(f"Duty set to{duty}")

# The HTML form sends this (works)
@app.route('/control', methods=['POST'])
def control():
    global counter
    command = request.form.get('command')
    
    if command == "left":
        print("left")
        motors.motor_forward(duty)
        socketio.emit('message', {'value': 'Recieved left','counter': str(counter), 'command': 'Left'})

    elif command == "right":
        print("right")
        motors.motor_backward(duty)
        socketio.emit('message', {'value': 'Recieved right','counter': str(counter), 'command': 'Right'})        

    elif command == "stop":
        print("stop")
        motors.stop()
        socketio.emit('message', {'value': 'Recieved stop', 'command': 'Stop'})
        image_base64 = encode_image_from_file()
        if image_base64:
            socketio.emit('image_update', {'image': image_base64})
    
    return "", 204  # No content response, just to acknowledge the request

def encode_image_from_file():
    if os.path.exists("/home/vision/Documents/v2/output.jpg"):
        with open("/home/vision/Documents/v2/output.jpg", "rb") as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')
    return None

def read_detections_from_file(filename="detections.txt"):
    """Reads the detections from a file and returns a list of (object, score)."""
    detections = []
    
    # Ensure the file exists
    if os.path.exists(filename):
        with open(filename, "r") as file:
            lines = file.readlines()
            for line in lines:
                # Split each line into object and score
                obj, score = line.strip().split(":")
                detections.append((obj, float(score)))
    
    return detections


if __name__ == "__main__":
    #app.run(host="0.0.0.0", port=8500)
    socketio.run(app, host="0.0.0.0", port=8500)
