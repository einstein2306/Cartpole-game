from flask import Flask, render_template
from flask_socketio import SocketIO
from models.load_model import CartpoleModel
import threading
import time

app = Flask(__name__)

socket = SocketIO(app, manage_session=False)

gif_data = None

def generate():
    global gif_data, len_frames
    while True:
        gif_data, len_frames = CartpoleModel()
        socket.emit("animation_gif", {"gif_data": gif_data})
        time.sleep(15)

threading.Thread(target=generate, daemon=True).start()

@socket.on("connect")
def connection():
    print("user connected.")

@app.route('/')
def main():
    return render_template('Main.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/AiMode')
def AIMode():
    if gif_data is None:
        mess = 'Program running has been started.'
        return render_template('AiMode.html', mess=mess)
    return render_template('AiMode.html', gif_data=gif_data)

@app.route('/UserMode')
def UserMode():
    return render_template("usermode.html")

if __name__ == "__main__":
    socket.run(app,debug=True)