from flask import Flask, render_template, session
from flask_session import Session
from flask_cors import CORS
from flask_socketio import SocketIO
from datetime import timedelta
import redis
from models.load_model import CartpoleModel
from models.text_gen import generate_text
import threading
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cartpole123'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'redis'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_REDIS'] = redis.Redis(
    host='redis-15972.c9.us-east-1-4.ec2.redns.redis-cloud.com', 
    port=15972,
    password='vFgcMIV4eFetaXi6f1gzTvvav7dwWvbz'
)
Session(app)
CORS(app)
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

@app.route('/Algorithm')
def algorithm():
    return render_template('algorithm.html')

@app.route('/AiMode')
def AIMode():
    if gif_data is None:
        mess = 'Program running has been started.'
        return render_template('AiMode.html', mess=mess)
    return render_template('AiMode.html', gif_data=gif_data)

@app.route('/UserMode')
def UserMode():
    return render_template("usermode.html")

@app.route("/RlBot")
def RlBot():
    if "chat_history" not in session:
        session["chat_history"] = []
    return render_template("dqn_assist.html", message=session['chat_history'])

@socket.on("new_message")
def handle_new_message(data):
    prompt = data.get("prompt", "")
    if not prompt:
        socket.emit("chat_response", {"error": "Empty prompt."})
        return

    if "chat_history" not in session:
        session["chat_history"] = []

    conversation = ""
    for chat in session["chat_history"]:
        conversation += f"{chat['prompt']}\n{chat['response']}\n"
    conversation += f"{prompt}\n"

    response = generate_text(conversation)

    session["chat_history"].append({
        "prompt": prompt,
        "response": response
    })
    session.modified = True

    socket.emit("chat_response", {
        "prompt": prompt,
        "response": response
    })

if __name__ == "__main__":
    socket.run(app,debug=True)