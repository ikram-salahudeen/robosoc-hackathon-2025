from flask import Flask, render_template

app = Flask(__name__, template_folder="web")

@app.route('/')
def home():
   return render_template('index.html')
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8500)
    

"""
@app.route('/left', methods=['POST'])
def left():
    print("left")
    return "left", 200

@app.route('/right', methods=['POST'])
def right():
    print("right")
    return "right", 200

@app.route('/stop', methods=['POST'])
def stop():
    print("stop")
    return "stop", 200

def update_text():
    global dynamic_text
    while True:
        new_text = input("Enter new text for the webpage: ")
        dynamic_text = new_text
"""

