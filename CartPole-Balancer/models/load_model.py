import os


os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

#import hashlib
import gymnasium as gym
from stable_baselines3 import DQN
from io import BytesIO
from PIL import Image
import base64
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.vec_env import DummyVecEnv
#import numpy as np

def CartpoleModel():
    env = gym.make("CartPole-v1",render_mode="rgb_array")
    env = Monitor(env)
    env = DummyVecEnv([lambda:env])
    model = DQN.load("logs/dqn/CartPole-v1_1/best_model.zip", env=env)

    frames=[]
    #t = 0
    #t_angle=[]
    
    for _ in range(1):
        obs = env.reset()

        while True:

            action, _ = model.predict(obs,deterministic=False)
            obs,_ , done, _  = env.step(action)
            #angle = abs(obs[0][2])
            #t_angle.append(angle)
            #t = t+1
            
            frames.append(env.render())
        
        
            if done :
                break
    
    buffer = BytesIO()   
    images = [Image.fromarray(frame) for frame in frames]
    images[0].save(buffer,format="GIF",save_all=True,append_images=images[1:],duration=50,loop=1)
    buffer.seek(0)
    gif_data = base64.b64encode(buffer.read()).decode('utf-8')
        
    return gif_data , len(frames)
    #return t_angle,t


#l1,t = CartpoleModel()
#print(l1)
#print(t)

"""

if __name__ == "__main__":


    global gif_data , total_frames
    data = None
    while True:
        
        new_data , new_total_frames = CartpoleModel()
        new_data = hashlib.md5(new_data).hexdigest()
        if data is None or data != new_data:
            data = new_data
            total_frames = new_total_frames
            print("It is updating..")
    
        else:
            print('it is same')
            
"""





        
    

        