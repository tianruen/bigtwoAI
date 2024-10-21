### preprocess the card game into features
from typing import List
import itertools

import big_two_AI as bt

class Preprocess:
    def __init__(self, game: bt.BigTwoGame) -> None:
        self.game = game
        self.cur_player = game.cur_player
        self.game_hist = game.game_hist
        self.all_cards = [bt.Card(suit, rank) for rank in bt.Card.ranks for suit in bt.Card.suits]
        self.large_cards = self.all_cards[-12:]
        
    def get_hand_cards(self) -> List:
        hand_card = set(self.cur_player.hand)
        return [1 if card in hand_card else 0 for card in self.all_cards]
    
    def get_opponent_num_cards(self) -> List:
        opponents = []
        self_idx = self.game.players.index(self.cur_player)
        
        for i in range(1,4):
            opp = self.game.players[(self_idx+i)%4]
            opponents.extend([1 if len(opp.hand) == i else 0 for i in range(1,14)])
        
        # for player in self.game.players:
        #     if player.name != self.cur_player.name:
        #         opponents.extend([1 if len(player.hand) == i else 0 for i in range(1,14)])
        return opponents
    
    def check_large_cards(self) -> List:
        # check which large cards have been played, from K to 2
        game_hist = [p_c[1] for p_c in self.game_hist if p_c[1] is not None]   # this is a nested list
        game_hist = list(itertools.chain(*game_hist))
        return [1 if card in game_hist else 0 for card in self.large_cards]
    
    def get_history(self) -> List:
        game_hist = [p_c[1] for p_c in self.game_hist if p_c[1] is not None]   # this is a nested list
        game_hist = list(itertools.chain(*game_hist))
        return [1 if card in game_hist else 0 for card in self.all_cards]
        
    def create_features(self) -> List:
        features = []
        features.extend(self.get_hand_cards())
        features.extend(self.get_opponent_num_cards())
        # features.extend(self.check_large_cards())
        features.extend(self.get_history())
        return features

# note: order of how we store doesn't matter since it's just a look up table
# single cards
# single = set([(bt.Card(s, r),) for s in bt.Card.suits for r in bt.Card.ranks])
single = [(bt.Card(s, r),) for s in bt.Card.suits for r in bt.Card.ranks]
# double cards
# double = set([(bt.Card(s[0], r), bt.Card(s[1], r)) for s in list(itertools.combinations(bt.Card.suits, 2)) for r in bt.Card.ranks])
double = [(bt.Card(s[0], r), bt.Card(s[1], r)) for s in list(itertools.combinations(bt.Card.suits, 2)) for r in bt.Card.ranks]
# triple cards
# triple = set([(bt.Card(s[0], r), bt.Card(s[1], r), bt.Card(s[2], r)) for r in bt.Card.ranks for s in list(itertools.combinations(bt.Card.suits, 3))])
triple = [(bt.Card(s[0], r), bt.Card(s[1], r), bt.Card(s[2], r)) for r in bt.Card.ranks for s in list(itertools.combinations(bt.Card.suits, 3))]
# five cards
suits_combo = list(itertools.product(bt.Card.suits, repeat=5))
ranks_combo = [bt.Card.ranks[i-5:i] for i in range(5, 14)]
straight = [tuple([bt.Card(s[i], r[i]) for i in range(5)]) for s in suits_combo for r in ranks_combo]
flush = [tuple([bt.Card(s, r[i]) for i in range(5)]) for s in bt.Card.suits for r in list(itertools.combinations(bt.Card.ranks, 5))]
full_house = [tuple(list(tri) + list(dou)) for tri in triple for dou in double if dou[0].rank != tri[0].rank]
four_one = [tuple([bt.Card(s, r) for s in bt.Card.suits] + [sin]) for r in bt.Card.ranks for sin in single if r != sin[0].rank]
five = set(straight) | set(flush) | set(full_house) | set(four_one)
five = list(five)
# all actions
# all_actions = single | double | triple | five
all_actions = single + double + triple + five
# create hash table to map actions to numbers and vice versa
act_to_num = {act : idx for idx, act in enumerate(all_actions)}
num_to_act = {idx : act for idx, act in enumerate(all_actions)}

### for testing
# p1, p2, p3, p4 = "A", "B1", "B2", "B3"
# t1, t2, t3, t4 = "Agent", "Bot", "Bot", "Bot"
# p_t = zip([p1,p2,p3,p4], [t1,t2,t3,t4])
# game = bt.BigTwoGame(p_t)
# # p = Preprocess(game)

# while not game.game_over():
#     cur_player = game.cur_player
#     table_card = next((p_c[1] for p_c in game.game_hist[-3:][::-1] if p_c[1] is not None), None)
    
#     # if cur_player.type in ["Agent", "AI"]:
#     #     p = Preprocess(game)
#     #     print("----")
#     #     print(f"Check {p.cur_player}'s features")
#     #     print(f"Hand Cards: {cur_player.hand}")
#     #     print(f"Hand Cards: {p.get_hand_cards()}")
#     #     print("-")
#     #     print([len(player.hand) for player in game.players if player.type not in ["Agent", "AI"]])
#     #     print(f"Opponent Cards: {p.get_opponent_num_cards()}")
#     #     print("-")
#     #     print(f"History: {game.game_hist}")
#     #     print(f"Large Cards: {p.check_large_cards()}")
#     #     print("----")
    
#     p = Preprocess(game)
#     print(f"Hand Cards: {cur_player.hand}")
#     print(torch.tensor(p.create_features()))
        
#     # else:
#     avail_act = cur_player.get_available_actions(table_card)
#     action = cur_player.get_action(avail_act)

#     # print(cur_player.name)
#     # print(f"Available action: {avail_act}")
#     # print(f"Played: {action}")
#     print(f"{cur_player.name} played {action}")
        
#     game.play_turn(action)
# game.display_winner()

# card_hist = [p_c[1] for p_c in game.game_hist if p_c[1] is not None]
# card_hist
# list(itertools.chain(*card_hist))