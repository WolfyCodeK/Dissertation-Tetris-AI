import csv
import os
import sys
import numpy as np
from environments.test_env import TestTetrisEnv
from itertools import count
from utils.screen_sizes import ScreenSizes
import utils.game_analysis as gu

import torch
import torch.nn as nn
import torch.nn.functional as F

# Code adapted from -> https://pytorch.org/tutorials/intermediate/reinforcement_q_learning.html

class DQN(nn.Module):
    def __init__(self, n_observations, n_actions):
        super(DQN, self).__init__()
        self.layer1 = nn.Linear(n_observations, 2048)
        self.layer2 = nn.Linear(2048, 2048)
        self.layer3 = nn.Linear(2048, 2048)
        self.layer4 = nn.Linear(2048, 2048)
        self.layer5 = nn.Linear(2048, n_actions)

    # Called with either one element to determine next action, or a batch
    # during optimization. Returns tensor([[left0exp,right0exp]...]).
    def forward(self, x):
        x = F.relu(self.layer1(x))
        x = F.relu(self.layer2(x))
        x = F.relu(self.layer3(x))
        x = F.relu(self.layer4(x))
        return self.layer5(x)

def get_flatterned_obs(state):
    # Extract numerical values from the dictionary
    numerical_values = [state[key].flatten() for key in state]

    # Concatenate the numerical values into a single array
    return np.concatenate(numerical_values)
    
def select_action(state):
    with torch.no_grad():
        return policy_net(state).max(1).indices.view(1, 1)

# Load model function
def load_model(model):
    file_path = 'tetris_model.pth'
    
    if os.path.exists(file_path):
        checkpoint = torch.load(file_path, map_location=torch.device(device_type))
        model.load_state_dict(checkpoint['model_state_dict'])
        
        return model
    else:
        print(f"Requested model not found!")
        exit(0)
        
def print_scores():
    title = "| Max Score | Max B2B | Max Pieces Placed | APS |"
    line = "-" * len(title)
    os.system('clear')
    print("> Game Analytics: ")
    print("")
    print(line)
    print("| Max Score | Max B2B | Max Pieces Placed | APS |")
    print(line)
    print("| {:^10}|".format(max_score), end="")
    print("{:^9}|".format(max_b2b), end="")
    print("{:^19}|".format(max_pieces_placed), end="")
    
    if aps == 0:
        print("{:^5}|".format("MAX"))
    else:
        print("{:^5}|".format(f"{aps}."))
        
    print(line)

if __name__ == '__main__':
    screen_size = ScreenSizes.MEDIUM
    playback_aps = 10
    
    if len(sys.argv) > 1:
        if sys.argv[1] != "":
            screen_size = int(sys.argv[1])

        if sys.argv[2] != "":
            playback_aps = int(sys.argv[2])
    
    env = TestTetrisEnv()
    
    env.render(screen_size=screen_size, show_fps=False, show_score=True, show_queue=True, playback=True, playback_aps=playback_aps)

    # if GPU is to be used
    device_type = "cuda" if torch.cuda.is_available() else "cpu"
    device = torch.device(device_type)

    # Get number of actions from gym action space
    n_actions = env.action_space.n
    # Get the number of state observations
    state, info = env.reset()
    n_observations = len(get_flatterned_obs(state))

    policy_net = DQN(n_observations, n_actions).to(device)
    
    policy_net = load_model(policy_net)
    policy_net.eval()

    max_score = 0
    max_b2b = 0
    max_pieces_placed = 0
    mistakes = 0
    last_gaps = 0
    
    if env.window_exists():
        aps = env.playback_aps
        
    # Create csv file to save data to
    with open('results.csv', 'w', newline='') as outcsv:
        writer = csv.writer(outcsv)
        writer.writerow(['pieces dropped', 'total score', 'max b2b', 'line clears', 'mistakes (%)'])

    while True:
        # Initialize the environment and get its state
        state, info = env.reset()
        
        state = torch.tensor(get_flatterned_obs(state), dtype=torch.float32, device=device).unsqueeze(0)
        
        for t in count():      
            action = select_action(state)

            observation, terminated, _ = env.step(action.item())
            
            new_gaps = gu.get_num_of_top_gaps(env._game) + gu.get_num_of_full_gaps(env._game)
            
            if new_gaps > last_gaps:
                last_gaps = new_gaps
                mistakes += 1

            if terminated:
                state = None
            else:
                state = torch.tensor(get_flatterned_obs(observation), dtype=torch.float32, device=device).unsqueeze(0)

            if terminated:
                with open('results.csv','a') as fd:
                    row = [env._game.piece_manager.num_of_pieces_dropped, env._game.score, env._game.max_b2b, env._game.lines_cleared, round((mistakes / env._game.piece_manager.num_of_pieces_dropped * 100), 2)]
                    
                    mistakes = 0
                    last_gaps = 0
                    new_gaps = 0
                    
                    if env._game.piece_manager.num_of_pieces_dropped > 3:
                        fd.write(','.join(str(x) for x in row))
                        fd.write('\n')
                break
