from flask import Flask, render_template
from models.load_model import CartpoleModel
from flask_socketio import SocketIO
from models.user import CartPoleGame
import threading
import time


game = CartPoleGame()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cartpole123'
socket = SocketIO(app)

gif_data = None

def generate():
        global gif_data , len_frames

        while True:
             gif_data, len_frames = CartpoleModel()
             socket.emit("animation_gif",{"gif_data": gif_data})
             time.sleep(10)

threading.Thread(target=generate,daemon=True).start()

@socket.on("connect")
def connection():
     print("user connected.")
    
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/Algorithm')
def algorithm():
    return render_template('algorithm.html')



@app.route('/AiMode')
def AIMode():
    if gif_data is None:
         mess = 'Program running has been started.'
         return render_template('AiMode.html',mess=mess)

    return render_template('AiMode.html',gif_data=gif_data)


@app.route('/UserMode')
def UserMode():
     return render_template("usermode.html")


@socket.on("action")
def step(data):
    """
    Perform a step in the environment based on the user's action.
    """
    action = 0 if data['action'] == "left" else 1  # Default to 0 if no action is provided
    frame, done = game.step(action)
    socket.emit('frame',{'frame':frame,'done':done})

@socket.on("reset")
def reset():
    """
    Reset the CartPole environment.
    """
    frame = game.reset()
    socket.emit('frame',{'frame':frame,'done':False})





if __name__ == "__main__":
    
    socket.run(app,debug=True)
    
