from gym_tetris_env import TetrisEnv, ScreenSizes
from stable_baselines3 import PPO
import os
from datetime import datetime

if __name__ == '__main__':
    logs_directory = f"logs/{datetime.now().strftime('%Y-%m-%d---%H-%M-%S')}/"
    models_directory = f"models/{datetime.now().strftime('%Y-%m-%d---%H-%M-%S')}/"

    if not os.path.exists(logs_directory):
        os.makedirs(logs_directory)

    if not os.path.exists(models_directory):
        os.makedirs(models_directory)
    
    env = TetrisEnv()
    env.render(screen_size=ScreenSizes.XXSMALL, show_fps=True, show_score=True)
    env.reset()
    env.seed(0)

    model = PPO('MultiInputPolicy', env, verbose=0, tensorboard_log=logs_directory, learning_rate=0.0003)
    # model = PPO.load("models/2023-11-27---21-29-40/400000.zip", env=env)
    model.verbose = 0

    STEPS = 20000
    count = 0
    
    print("Training agent...")
    
    while True:
        count += 1
        model.learn(total_timesteps=STEPS, reset_num_timesteps=False, tb_log_name=f"PPO", progress_bar=True)
        model.save(f"{models_directory}/{STEPS*count}")