import cv2
import base64
import numpy as np
from flask import Flask, render_template
from flask_socketio import SocketIO
from modlib.apps import Annotator
from modlib.devices import AiCamera
from modlib.models.zoo import SSDMobileNetV2FPNLite320x320

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")  # Enable WebSockets

# Initialize AI Camera and Model
device = AiCamera()
model = SSDMobileNetV2FPNLite320x320()
device.deploy(model)
annotator = Annotator(thickness=1, text_thickness=1, text_scale=0.4)

@app.route('/')
def index():
    """Render HTML page with WebSocket video stream."""
    return render_template('index.html')

def generate_frames():
    """Continuously capture and send frames via WebSocket."""
    with device as stream:
        for frame in stream:
            detections = frame.detections[frame.detections.confidence > 0.55]
            labels = [f"{model.labels[class_id]}: {score:0.2f}" for _, score, class_id, _ in detections]
            
            annotator.annotate_boxes(frame, detections, labels=labels)

            # Convert frame to JPEG format
            _, buffer = cv2.imencode('.jpg', frame.array)
            frame_bytes = buffer.tobytes()
            
            # Encode to Base64 for WebSockets
            frame_base64 = base64.b64encode(frame_bytes).decode('utf-8')

            # Send frame via WebSocket
            socketio.emit('video_frame', {'image': frame_base64})

@socketio.on('start_stream')
def start_stream():
    """Start video stream when client connects."""
    generate_frames()

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
