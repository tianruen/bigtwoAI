from collections import deque
import random
import pandas as pd
import torch

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
        
    def self_play(self, model, mcts_iter=100, c_param=1.4, tau=1.5):
        self.num_match += 1
        p1, p2, p3, p4 = "A", "B", "C", "D"
        t1, t2, t3, t4 = "Agent", "Agent", "Agent", "Agent"
        p_t = zip([p1,p2,p3,p4], [t1,t2,t3,t4])
        game = bt.BigTwoGame(p_t)
        
        if self.num_match % 10 == 0:
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
            
            if self.num_match % 10 == 0:
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
        
        if self.num_match % 10 == 0:
            df = pd.DataFrame(self.memory, columns=["num_match", "features", "dist", "reward"])
            df.to_csv(f"memory_{self.num_match}.csv", index=False)
        
        return short_memory
        
    def train_short_memory(self, state, action_dist, rewards):
        self.model.train(state, action_dist, rewards)
        
    def train_long_memory(self):
        if len(self.memory) > self.batch_size:
            mini_sample = random.sample(self.memory, self.batch_size)
        else:
            mini_sample = self.memory
        _, state, action_dist, rewards = zip(*mini_sample)
        self.model.train(state, action_dist, rewards)
        
def train():
    agent = Agent()
    for i in range(1000):
        short_mem = agent.self_play(agent.model, mcts_iter=200, c_param=5, tau=3)
        _, state, action_dist, rewards = zip(*short_mem)
        agent.train_short_memory(state, action_dist, rewards)
        agent.train_long_memory()
        
        if (i+1) % 10 == 0:
            torch.save(agent.model.state_dict(), f"alphazero_{i+1}.pt")

if __name__ == "__main__":
    train() 