from collections import deque, defaultdict
import random
import pandas as pd
import torch
import time
import argparse
import datetime
import os
import json

import big_two_AI as bt
import mcts
import preprocess
import alphazero as az
import model

def test(save_path):
    # define save path
    time_ = datetime.datetime.now().strftime('%Y%m%d_%H%M')
    if args.save_path: save_path = args.save_path
    else: save_path = "test_" + time_
    os.makedirs(save_path, exist_ok=True)
    
    hidden_dim = 256
    a100 = model.deepPG(143, 18880, hidden_dim)
    a20 = model.deepPG(143, 18880, hidden_dim)
    a470 = model.deepPG(143, 18880, hidden_dim)
    a610 = model.deepPG(143, 18880, hidden_dim)

    #### change here for loading the model ####
    # a100.load_state_dict(torch.load(r"first_training_261024\alphazero.pt"))
    a100.load_state_dict(torch.load("first_training_261024/alphazero.pt"))
    a20.load_state_dict(torch.load("second_training_271024/alphazero_19.pt"))
    a470.load_state_dict(torch.load("training/20241107_1758/alphazero_470.pt"))
    a610.load_state_dict(torch.load("training/20241107_1758/alphazero_760.pt"))

    memory = deque(maxlen=100000)

    num_win = defaultdict(int)
    n = 200
    random_list = [i for i in range(4)]
    for i in range(n):
        player_list = ["A100", "A20", "A470", "A610"]
        type_list = ["Agent", "Agent", "Agent", "Agent"]
        random.shuffle(random_list)
        player_list = [player_list[r] for r in random_list]
        type_list = [type_list[r] for r in random_list]
        p_t = zip(player_list, type_list)
        game = bt.BigTwoGame(p_t)
        s = time.time()
        short_memory = []
        while not game.game_over():
            player_idx = game.players.index(game.cur_player)
            table_card = next((p_c[1] for p_c in game.game_hist[-3:][::-1] if p_c[1] is not None), None)
            
            if game.cur_player.type == "Agent":
                if f"node{player_idx}" not in locals():
                    mod_game = az.ModifyGame(game, player_idx)
                    state = az.BigTwoState(mod_game)
                    locals()[f"node{player_idx}"] = az.MCTSNode(state)
                else:
                    locals()[f"node{player_idx}"] = az.get_node(locals()[f"node{player_idx}"], game)
                
                ### change this part for selecting the model    
                if game.cur_player.name == "A100": model_ = a100
                if game.cur_player.name == "A20": model_ = a20
                if game.cur_player.name == "A470": model_ = a470
                if game.cur_player.name == "A610": model_ = a610
                
                # model_ = a100 if game.cur_player.name == "A100" else a20
                
                mcts_ = az.MCTS(locals()[f"node{player_idx}"])
                node, action, dist = mcts_.search(policy_network=model_, 
                                                num_iterations=100, 
                                                c_param=1.4, 
                                                tau=0.001,)
                
                p = preprocess.Preprocess(game)
                features = p.create_features()
                short_memory.append((player_idx, features, dist))
                
            else:
                avail_act = game.cur_player.get_available_actions(table_card)
                action = game.cur_player.get_action(avail_act)

            print(game.cur_player.name)
            print(f"Available action: {game.cur_player.get_available_actions(table_card)}")
            print(f"Played: {action}")
                
            game.play_turn(action)
        game.display_winner()
        e = time.time()
        
        winner_idx = game.players.index(game.winner)
        for i_, f, d in short_memory:
            if i_ == winner_idx:
                memory.append((game.players[i_].name, f, d, 1))
            else:
                memory.append((game.players[i_].name, f, d, -1))
        
        num_win[game.winner.name] += 1
        sorted_dict = dict(sorted(num_win.items(), key= lambda x: x[0]))
        # winner_idx = game.players.index(game.winner)
        # win_rate[winner_idx] += 1
        print(f"Game {i+1}")
        print(sorted_dict)
        print([wr/(i+1) for _, wr in sorted_dict.items()])
        print(f"Time taken: {(e-s)/60} minutes")
        print("-----------------------------")
        
    df = pd.DataFrame(memory, columns=["num_match", "features", "dist", "reward"])
    df.to_csv(f"{save_path}/memory_{i+1}.csv", index=False)
    
def parse_args():
    # create parser
    parser = argparse.ArgumentParser(description="Test AlphaZero models")
    # save path argument
    parser.add_argument("--save_path", type=str, default=None, help="Path to save the match data; default=None")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    test(args.save_path)