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

# single cards
single = [(bt.Card(s, r),) for s in bt.Card.suits for r in bt.Card.ranks]
# double cards
double = [tuple(sorted([bt.Card(s[0], r), bt.Card(s[1], r)])) for s in list(itertools.combinations(bt.Card.suits, 2)) for r in bt.Card.ranks]
# triple cards
triple = [tuple(sorted([bt.Card(s[0], r), bt.Card(s[1], r), bt.Card(s[2], r)])) for r in bt.Card.ranks for s in list(itertools.combinations(bt.Card.suits, 3))]
# five cards
suits_combo = list(itertools.product(bt.Card.suits, repeat=5))
ranks_combo = [bt.Card.ranks[i-5:i] for i in range(5, 14)]
straight = [tuple(sorted([bt.Card(s[i], r[i]) for i in range(5)])) for s in suits_combo for r in ranks_combo]
flush = [tuple(sorted([bt.Card(s, r[i]) for i in range(5)])) for s in bt.Card.suits for r in list(itertools.combinations(bt.Card.ranks, 5))]
full_house = [tuple(sorted(list(tri) + list(dou))) for tri in triple for dou in double if dou[0].rank != tri[0].rank]
four_one = [tuple(sorted([bt.Card(s, r) for s in bt.Card.suits] + list(sin))) for r in bt.Card.ranks for sin in single if r != sin[0].rank]
five = list(set(straight) | set(flush) | set(full_house) | set(four_one))
# all actions
all_actions = single + double + triple + five 
all_actions = sorted(all_actions) + [None]
# create hash table to map actions to numbers and vice versa
cards_to_num = {cards : idx for idx, cards in enumerate(all_actions)}
num_to_cards = {idx : cards for idx, cards in enumerate(all_actions)}
encode = lambda cards: cards_to_num[cards]
decode = lambda idx: num_to_cards[idx]
