from gymnasium import Env, spaces
import numpy as np
from src.YoshiWrapper import YoshiWrapper

class YoshiEnv(Env):
    def __init__(self):
        super(YoshiEnv, self).__init__()

        self.yoshi = YoshiWrapper()
        self.prev_step = self.yoshi.getCurrentStep()
        
        width, height = self.yoshi.gba.core.desired_video_dimensions()
        self.observation_space = spaces.Box(0, 255, [width, height, 3], dtype = np.uint8)
        self.action_space = spaces.Discrete(14)

    def step(self, action):
        terminate = False
        truncated = False

        self.yoshi.runFrame()
        self.yoshi.doAction(action)
        self.yoshi.timer.start()
        current_step = self.yoshi.getCurrentStep()

        if round((current_step) - (self.prev_step)) <= 0:
            reward = -0.1
        else:
            reward = 0.1

        if not self.yoshi.getMarioSafety():
            reward = -1
            terminate = True
        elif self.yoshi.timer.elapsed() >= 60:
            truncated = True
            reward = -1

        self.prev_step = current_step

        return self.yoshi.getScreen(), reward, terminate, truncated, {}

    def reset(self, seed = None, options = None):
        self.yoshi.timer.reset()
        self.prev_step = self.yoshi.getCurrentStep()
        self.yoshi.resetState()

        return self.yoshi.getScreen(), {}

    def render(self, mode='human'):
        pass