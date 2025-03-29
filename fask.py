from flask import Flask, render_template
from flask_socketio import SocketIO, emit

import distance

app = Flask(__name__, template_folder="web")

@socketio.on("my_event")
def poll():
    for x in range(5):
        distance_data = distance.get_distances()

        emit('server', {"distance1":1, "distance2":2}, room=sid)
        socketio.sleep(1)

@app.route('/')
def home():
   return render_template('index.html')
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8500)

@app.route('/control', methods=['POST'])
def control():
    command = request.form.get('command')
    
    if command == "left":
        print("left")
    elif command == "right":
        print("right")
    elif command == "stop":
        print("stop")
    
    return "", 204  # No content response

"""
def update_text():
    global dynamic_text
    while True:
        new_text = input("Enter new text for the webpage: ")
        dynamic_text = new_text
"""

