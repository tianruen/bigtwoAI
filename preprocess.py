### preprocess the card game into features
from typing import List
import big_two_AI as bt

class Preprocess:
    def __init__(self, game: bt.BigTwoGame) -> None:
        self.game = game
        self.cur_player = game.cur_player
        self.game_hist = game.game_hist
        self.all_cards = [bt.Card(suit, rank) for rank in bt.Card.ranks for suit in bt.Card.suits]
        
    def get_hand_cards(self) -> List:
        hand_card = set(self.cur_player.hand)
        return [1 if card in hand_card else 0 for card in self.all_cards]
    
    def get_opponent_num_cards(self):
        opponents = []
        for player in self.game.players:
            if player.name != self.cur_player.name:
                opponents.extend([1 if len(player.hand) == i else 0 for i in range(1,14)])
        return opponents




### for testing
p1, p2, p3, p4 = "A", "B1", "B2", "B3"
t1, t2, t3, t4 = "Agent", "Bot", "Bot", "Bot"
p_t = zip([p1,p2,p3,p4], [t1,t2,t3,t4])
game = bt.BigTwoGame(p_t)

game.cur_player

p = Preprocess(game)

p.cur_player
sum(p.get_hand_card())