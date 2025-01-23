from typing import List, Tuple, Optional
from fastapi import FastAPI
from pydantic import BaseModel
import torch
import time
import threading

import big_two_AI as bt
import alphazero as az
import preprocess as pp
import model

app = FastAPI()
agent = model.deepPG(143, 18880, 256)
agent.load_state_dict(torch.load("training/20241119_0224/alphazero_1000.pt"))

@app.get("/")
def read_root():
    return {"message": "BigTwo AI"}

class Cards(BaseModel):
    # game: bt.BigTwoGame
    hand_card: List[Tuple[str, str]]
    hist: List[Optional[List[Tuple[str, str]]]]
    opp1_num_cards: int
    opp2_num_cards: int
    opp3_num_cards: int
    
@app.post('/agent/get_action')
def get_action(input: Cards):
    input = input.model_dump()
    hand_card = input['hand_card']
    hist = input['hist']
    opp1_num_cards = input['opp1_num_cards']
    opp2_num_cards = input['opp2_num_cards']
    opp3_num_cards = input['opp3_num_cards']
    
    p1, p2, p3, p4 = "A", "B1", "B2", "B3"
    t1, t2, t3, t4 = "Agent", "Bot", "Bot", "Bot"
    p_t = zip([p1,p2,p3,p4], [t1,t2,t3,t4])
    game = bt.BigTwoGame(p_t)
    card = [bt.Card(c[0], c[1]) for c in hand_card]
    card.sort()
    game.players[0].hand = card
    played_cards = [[bt.Card(c[0], c[1]) for c in action] if action else None for action in hist]
    game.game_hist = [("_", c) for c in played_cards]
    
    mod_game = az.ModifyGame(game, player_idx=0)        # always set agent as player 0
    # get all cards played and agent's card
    ignore_cards = played_cards + mod_game.players[0].hand
    mod_game.players[1].hand = [c[0] for c in pp.single if c[0] not in ignore_cards]    # c is tuple with length 1
    mod_game.cur_player = mod_game.players[0]   # set cur_player to agent
    
    mod_game.original_game.cur_player = mod_game.players[0]   
    mod_game.original_game.players[1].hand = [i for i in range(opp1_num_cards)]     # update opponent's number of cards
    mod_game.original_game.players[2].hand = [i for i in range(opp2_num_cards)]
    mod_game.original_game.players[3].hand = [i for i in range(opp3_num_cards)]
    
    mod_game.original_game.game_hist = game.game_hist           # update game history
    
    state = az.BigTwoState(mod_game)
    node_ = az.MCTSNode(state)
    mcts_ = az.MCTS(node_)
    
    # s = time.time()
    search_done = False
    node, action, dist = mcts_.search(policy_network=agent, 
                                      num_iterations=200, 
                                      c_param=0.01, 
                                      tau=0.01,)
    search_done = True
    
    # dist_keys = [pp.decode(k) for k in dist.keys()]
    # dist = dict(zip(dist_keys, dist.values()))
    # action = max(dist, key=dist.get)    # get action with highest probability, rather than random sampling (which is what the orignal source code does)
    # print(f"Distribution: {dist}")
    
    
    return {
        'action': action,
        # 'distribution': dist,
    }
    
    
# {
#   "hand_card": [("Diamonds", "4"), ("Hearts", "4"), ("Diamonds", "5"), ("Spades", "6"), ("Clubs", "7"), ("Clubs", "8"), ("Hearts", "8"), ("Spades", "8"), ("Clubs", "10"), ("Spades", "Q"), ("Hearts", "2")],
#   "hist": [[("Diamonds", "3"), ("Clubs", "3")], [("Clubs", "4"), ("Spades", "4")], [("Diamonds", "6"), ("Hearts", "6")], [("Diamonds", "7"), ("Hearts", "7")]],
#   "opp1_num_cards": 11,
#   "opp2_num_cards": 11,
#   "opp3_num_cards": 11
# }


#   "hand_card": [["Diamonds", "4"], ["Hearts", "4"], ["Diamonds", "5"], ["Spades", "6"], ["Clubs", "7"], ["Clubs", "8"], ["Hearts", "8"], ["Spades", "8"], ["Clubs", "10"], ["Spades", "Q"], ["Hearts", "2"]],
#   "hist": [[["Diamonds", "3"], ["Clubs", "3"]], [["Clubs", "4"], ["Spades", "4"]], [["Diamonds", "6"], ["Hearts", "6"]], [["Diamonds", "7"], ["Hearts", "7"]]],