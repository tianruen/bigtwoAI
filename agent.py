from collections import deque
import random
import pandas as pd
import torch
import datetime
import argparse
import os
import json

import big_two_AI as bt
import mcts
import preprocess
import alphazero as az
import model

class Agent:
    def __init__(self, hidden_dim=256) -> None:
        self.model = model.deepPG(143, 18880, hidden_dim)
        self.memory = deque(maxlen=100000)
        self.batch_size = 64
        self.num_match = 0
        self.print_freq = 10
        
    def self_play(self, model, mcts_iter=100, c_param=1.4, tau=1.5):
        self.num_match += 1
        p1, p2, p3, p4 = "A", "B", "C", "D"
        t1, t2, t3, t4 = "Agent", "Agent", "Agent", "Agent"
        p_t = zip([p1,p2,p3,p4], [t1,t2,t3,t4])
        game = bt.BigTwoGame(p_t)
        
        if self.num_match % self.print_freq == 0:
            print(f"--------------Match {self.num_match}--------------")
        
        self_play_data = []
        while not game.game_over():
            player_idx = game.players.index(game.cur_player)
            
            if f"node{player_idx}" not in locals():
                mod_game = az.ModifyGame(game, player_idx)
                state = az.BigTwoState(mod_game)
                locals()[f"node{player_idx}"] = az.MCTSNode(state)
            else:
                locals()[f"node{player_idx}"] = az.get_node(locals()[f"node{player_idx}"], game)
                
            # node = MCTSNode(state)
            mcts_ = az.MCTS(locals()[f"node{player_idx}"])
            node, action, dist = mcts_.search(model, mcts_iter, c_param, tau)
            
            if self.num_match % self.print_freq == 0:
                print(game.cur_player.name)
                table_card = next((p_c[1] for p_c in game.game_hist[-3:][::-1] if p_c[1] is not None), None)
                print(f"Available action: {game.cur_player.get_available_actions(table_card)}")
                print(f"Played: {action}")
            
            p = preprocess.Preprocess(game)
            features = p.create_features()
            self_play_data.append((player_idx, features, dist))

            game.play_turn(action)

        game.display_winner()
        
        short_memory = []
        winner_idx = game.players.index(game.winner)
        for i, f, d in self_play_data:
            if i == winner_idx:
                short_memory.append((self.num_match, f, d, 1))
            else:
                short_memory.append((self.num_match, f, d, -1))
        self.memory.extend(short_memory)
        
        return short_memory
    
    def save_mem_to_csv(self, save_path):
        df = pd.DataFrame(self.memory, columns=["num_match", "features", "dist", "reward"])
        df.to_csv(f"{save_path}/memory_{self.num_match}.csv", index=False)
    
    def train_short_memory(self, state, action_dist, rewards, regularise_lambda=0):
        self.model.train(state, action_dist, rewards, regularise_lambda)
        
    def train_long_memory(self):
        if len(self.memory) > self.batch_size:
            mini_sample = random.sample(self.memory, self.batch_size)
        else:
            mini_sample = self.memory
        _, state, action_dist, rewards = zip(*mini_sample)
        self.model.train(state, action_dist, rewards)
        
def parse_args():
    # create parser
    parser = argparse.ArgumentParser(description="Train AlphaZero model")
    
    parser.add_argument("--save_path", type=str, default=None, 
                        help="Path to save the model; default=None")
    parser.add_argument("--model_path", type=str, default=None, 
                        help="Path to load the model; default=None")
    parser.add_argument("--num_match", type=int, default=None, 
                        help="Number of matches have been played; default=None")
    parser.add_argument("--print_freq", type=int, default=None, 
                        help="Printing frequency; default=None")
    parser.add_argument("--mcts_iter", type=int, default=200, 
                        help="Number of iterations per round in MCTS; default=200")
    parser.add_argument("--c_param", type=float, default=1.4, 
                        help="Exploration constant. Higher value favours more exploration by the agent; default=1.4")
    parser.add_argument("--tau", type=float, default=1.5, 
                        help="Temperature. The higher it is, the more uniform across the probability distribtuion of available actions; default=1.5")
    parser.add_argument("--regularise_lambda", type=float, default=0,
                        help="L2 regularisation parameter; default=0")
    parser.add_argument("--desc", type=str, default=None, 
                        help="Description of the training; default=None")
    return parser.parse_args()
        
def train():
    # parse arguments
    args = parse_args()
    
    # define save path
    time_ = datetime.datetime.now().strftime('%Y%m%d_%H%M')
    if args.save_path: save_path = args.save_path
    else: save_path = "training_" + time_
    os.makedirs(save_path, exist_ok=True)
    
    # save arguments into a json file
    with open(f"{save_path}/description.json", "w") as json_file:
        json.dump(vars(args), json_file, indent=4)  # `indent=4` makes the file more readable
    
    agent = Agent()
    if args.model_path:
        if not os.path.isfile(args.model_path):
            raise ValueError("The model path does not exist")
        agent.model.load_state_dict(torch.load(args.model_path))
    
    if args.num_match: agent.num_match = args.num_match
    if args.print_freq: agent.print_freq = args.print_freq
        
    for _ in range(1000):
        short_mem = agent.self_play(agent.model, mcts_iter=args.mcts_iter, c_param=args.c_param, tau=args.tau)
        _, state, action_dist, rewards = zip(*short_mem)
        agent.train_short_memory(state, action_dist, rewards, regularise_lambda=args.regularise_lambda)
        agent.train_long_memory()
        
        if agent.num_match % 10 == 0:
            torch.save(agent.model.state_dict(), f"{save_path}/alphazero_{agent.num_match}.pt")
            agent.save_mem_to_csv(save_path)

if __name__ == "__main__":
    train() 