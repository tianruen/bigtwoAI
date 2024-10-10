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
        for player in self.game.players:
            if player.name != self.cur_player.name:
                opponents.extend([1 if len(player.hand) == i else 0 for i in range(1,14)])
        return opponents
    
    def check_large_cards(self) -> List:
        # check which large cards have been played, from K to 2
        game_hist = [p_c[1] for p_c in self.game_hist if p_c[1] is not None]   # this is a nested list
        game_hist = list(itertools.chain(*game_hist))
        return [1 if card in game_hist else 0 for card in self.large_cards]
    
    def create_features(self) -> List:
        features = []
        features.extend(self.get_hand_cards())
        features.extend(self.get_opponent_num_cards())
        features.extend(self.check_large_cards())
        return features

### for testing
p1, p2, p3, p4 = "A", "B1", "B2", "B3"
t1, t2, t3, t4 = "Agent", "Bot", "Bot", "Bot"
p_t = zip([p1,p2,p3,p4], [t1,t2,t3,t4])
game = bt.BigTwoGame(p_t)

while not game.game_over():
    cur_player = game.cur_player
    table_card = next((p_c[1] for p_c in game.game_hist[-3:][::-1] if p_c[1] is not None), None)
    
    if cur_player.type in ["Agent", "AI"]:
        p = Preprocess(game)
        print("----")
        print("Check A's features")
        print(f"Hand Cards: {cur_player.hand}")
        print(f"Hand Cards: {p.get_hand_cards()}")
        print("-")
        print([len(player.hand) for player in game.players if player.type not in ["Agent", "AI"]])
        print(f"Opponent Cards: {p.get_opponent_num_cards()}")
        print("-")
        print(f"History: {game.game_hist}")
        print(f"Large Cards: {p.check_large_cards()}")
        print("----")
        
    # else:
    avail_act = cur_player.get_available_actions(table_card)
    action = cur_player.get_action(avail_act)

    # print(cur_player.name)
    # print(f"Available action: {avail_act}")
    # print(f"Played: {action}")
    print(f"{cur_player.name} played {action}")
        
    game.play_turn(action)
game.display_winner()

card_hist = [p_c[1] for p_c in game.game_hist if p_c[1] is not None]
card_hist
list(itertools.chain(*card_hist))