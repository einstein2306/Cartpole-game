import gymnasium as gym
import cv2

class CartPoleGame:
    def __init__(self):
        self.env = gym.make('CartPole-v1', render_mode="rgb_array")
        self.state = self.env.reset()

    def step(self, action):
        """
        Perform a step in the environment with the given action.
        """
        self.state, _, done, _, _ = self.env.step(action)
        frame = self.env.render()
        resized_frame = cv2.resize(frame,(600,400))
        if done:
            self.reset()
        return resized_frame.flatten().tolist(), done

    def reset(self):
        """
        Reset the environment and return the initial state.
        """
        self.state, _ = self.env.reset()
        frame = self.env.render()
        resized_frame = cv2.resize(frame,(600,400))
        return resized_frame.flatten().tolist()