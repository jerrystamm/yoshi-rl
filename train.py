from stable_baselines3 import PPO
from gymnasium.wrappers import GrayScaleObservation
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.vec_env import VecFrameStack, SubprocVecEnv
from src.YoshiEnv import YoshiEnv

def make_env():
    env = YoshiEnv()
    env = Monitor(env, "./logs/")
    env = GrayScaleObservation(env, keep_dim = True)
    return env

def train_model():

    num_envs = 1
    env = SubprocVecEnv([make_env for _ in range(num_envs)])
    env = VecFrameStack(env, 4, channels_order='last')

    model = PPO("CnnPolicy", env, verbose=1, tensorboard_log="./logs/", device='cuda')
    
    model.learn(total_timesteps=3000000)
    model.save("yoshi_train")

    env.close()

if __name__ == '__main__': 
    train_model()