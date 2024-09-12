import random
from collections import Counter
import re

class Card:
    suits = ['Diamonds', 'Clubs', 'Hearts', 'Spades']
    ranks = ['3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A', '2']
    
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __repr__(self):
        return f"{self.rank} of {self.suit}"
    
    def __lt__(self, other):
        if self.rank == other.rank:
            return self.suits.index(self.suit) < self.suits.index(other.suit)
        return self.ranks.index(self.rank) < self.ranks.index(other.rank)
    
    def __eq__(self, value: object) -> bool:
        if isinstance(value, Card):
            return self.suit == value.suit and self.rank == value.rank
        return False
    
    def __hash__(self):
        return hash((self.suit, self.rank))
    
class Deck:
    def __init__(self):
        self.cards = [Card(suit, rank) for suit in Card.suits for rank in Card.ranks]
        random.shuffle(self.cards)

    def deal(self, num_hands):
        hands = []
        for i in range(num_hands):
            hands.append(self.cards[i::num_hands])
        return hands
    
class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []

    def receive_cards(self, cards):
        self.hand.extend(cards)
        self.hand.sort()

    def play_cards(self, cards):
        for card in cards:
            self.hand.remove(card)

    def __repr__(self):
        return f"{self.name}: {self.hand}"
    
class Hand:
    def __init__(self, cards):
        self.cards = cards
        self.cards.sort()
        self.cards_length = len(self.cards)
        
    def is_valid(self, cards2=None):
        uniq_rank = set([c.rank for c in self.cards])
        
        if cards2 is None:
            cards2 = self.cards
        
        if len(self.cards) != len(cards2):
            return False
        if self.cards_length == 1:
            return True
        elif self.cards_length == 2 or self.cards_length == 3:
            return len(uniq_rank) == 1
        elif self.cards_length == 5:
            return self.suitsIsSame(self.cards) or self.isStraight(self.cards) or len(uniq_rank) == 2
            # tong hua/same pattern & tong hua shun OR straight OR 3 of a kind/full house & 4 of a kind

        return False
    
    def suitsIsSame(self, cards):
        first_suit = cards[0].suit
        for i in range(1, len(cards)):
            if cards[i].suit != first_suit:
                return False
        return True
    
    def isStraight(self, cards):
        assert len(cards) == 5
        for i in range(4):
            c = cards[i]
            next_rank = c.ranks[c.ranks.index(c.rank) + 1]
            if next_rank != cards[i+1].rank:
                return False
        return True
    
    def compare(self, cards2): # compare the value between self.cards and cards2. True if self.cards > cards2, else False
        cards2.sort()
        if self.cards_length in [1,2,3]:    # for each cards, the rank needs to be the same
            return self.cards[-1] > cards2[-1]
        elif self.cards_length == 5:
            return self.compare5(cards2)
        
    def compare5(self, cards2):
        cards2.sort()
        
        c1_pattern = self.five_cards_pattern(self.cards)
        c2_pattern = self.five_cards_pattern(cards2)
        
        if c1_pattern[0] == c2_pattern[0]:
            if c1_pattern[0] in [0,1,4]:    # royal flush/tong hua shun or same pattern/tong hua or straight
                return c1_pattern[1] > c2_pattern[1]
            if c2_pattern[0] in [2,3]:    # 4 of a kind or full house/3 of a kind
                return c1_pattern[1] > c2_pattern[1] # check rank value
        else:
            return c1_pattern[0] > c2_pattern[0]
        
    def five_cards_pattern(self, cards):
        assert len(cards) == 5
        cards.sort()
        
        rank_counter = Counter([c.rank for c in cards])
        most_repeated_rank = max(rank_counter, key=rank_counter.get)
        
        # royal flush / tong hua shun
        if self.isStraight(cards) and self.suitsIsSame(cards):
            return (4, max(cards))
        # 4 of a kind
        if max(rank_counter.values) == 4:
            return (3, most_repeated_rank)
        # full house / 3 of a kind
        if max(rank_counter.values) == 3:
            return (2, most_repeated_rank)
        # same pattern / tong hua
        if self.suitsIsSame(cards):
            return (1, max(cards))
        # straight / shun
        if self.isStraight(cards):
            return (0, max(cards))
        
class BigTwoGame:
    def __init__(self, player_names):
        self.players = [Player(name) for name in player_names]
        self.deck = Deck()
        self.distribute_cards()
        
    def distribute_cards(self):
        hands = self.deck.deal(len(self.players))
        for player, hand in zip(self.players, hands):
            player.receive_cards(hand)
            
    def play_game(self):
        cur_player = self.starting_player()               # find the starting player
        cur_card = None
        skip_time = 0
        while not self.game_over():
            print(f"{cur_player.name}'s turn")
            print(f"{cur_player.name}'s cards: {cur_player.hand}")
            print(f"Cards on table: {cur_card}")

            playing = input("Do you want to play cards? (y/n): ").lower()

            if playing == 'y':
                skip_time = 0
                cards_before_play = cur_player.hand.copy()
                self.play_turn(cur_player, cur_card)                  # current player plays card
                cur_card = list(set(cards_before_play) - set(cur_player.hand))
                cur_player = self.next_player(cur_player)   # find next player
            else:
                skip_time = skip_time + 1       # if all three player skip, the game is reset
                if skip_time > 2:
                    cur_card = None
                cur_player = self.next_player(cur_player)
                continue

        self.display_winner(cur_player)
        
    def starting_player(self):
        for player in self.players:
            for card in player.hand:
                if card.suit == 'Diamonds' and card.rank == '3':
                    return player
        return self.players[0]
    
    def next_player(self, cur_player):
        cur_index = self.players.index(cur_player)
        return self.players[(cur_index + 1) % len(self.players)]
    
    def play_turn(self, player, cur_cards):
        cards_to_play = input("Please input the card(s). Rank first then suit (e.g. 9D for 9 of Diamonds) :")
        cards_to_play = re.findall(r"([^,\s]+)", cards_to_play)
        # alternatively can use: card_to_play = card_to_play.split(",") (but whitespace won't be ignore)

        c_list = []
        for c in cards_to_play:
            if c[-1] == 'D':
                s = 'Diamonds'
            elif c[-1] == 'C':
                s = 'Clubs'
            elif c[-1] == 'H':
                s = 'Hearts'
            elif c[-1] == 'S':
                s = 'Spades'
            
            if c[0] == '1':
                r = '10'
            else:
                r = c[0]
            c_list.append(Card(s,r))
        
        exist = True
        for c in c_list:
            if c not in player.hand:
                exist = False
                break

        hand = Hand(c_list)
        valid = hand.is_valid(cur_cards)
        bigger = hand.compare(cur_cards)
        
        if not valid or not bigger or not exist:
            self.play_turn(player, cur_cards)
        else:
            # print(cards_to_play, c_list)
            player.play_cards(c_list)
            # print(f"{player.name} played: {cards_to_play}")
            print(f"{player.name} played: {c_list}")
            
    def game_over(self):
        return any([len(player.hand) == 0 for player in self.players])
    
    def display_winner(self, player):
        print(f"{player.name} is the winner")
        
if __name__ == "__main__":
    p1 = input("First player name: ")
    p2 = input("Second player name: ")
    p3 = input("Third player name: ")
    p4 = input("Fourth player name: ")
    players = [p1,p2,p3,p4]

    game = BigTwoGame(players)
    game.play_game()