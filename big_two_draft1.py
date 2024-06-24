import random
from collections import Counter
import re

class Card:
    suits = ['Diamonds', 'Clubs', 'Hearts', 'Spades']
    # suits = ['D', 'C', 'H', 'S']
    ranks = ['3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A', '2']
    rank2val = {rank:i for i,rank in enumerate(ranks)}
    suit2val = {suit:i for i,suit in enumerate(suits)}

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
        self.cards = self.sort_cards(cards)
        self.cards_length = len(self.cards)
        self.suit_dict = {c: Card.rank2val[c.rank] for c in self.cards}
        self.rank_dict = {c: Card.rank2val[c.rank] for c in self.cards}
        
    def sort_cards(self, cards):
        suit_dict = {c: Card.suit2val[c.suit] for c in cards}
        cards = [l[0] for l in sorted(suit_dict.items(), key=lambda item: item[1])]
        rank_dict = {c: Card.rank2val[c.rank] for c in cards}
        cards = [l[0] for l in sorted(rank_dict.items(), key=lambda item: item[1])]
        return cards

    def is_valid(self, cards2):
        uniq_rank = list(set(self.rank_dict.values()))

        if cards2 is None:
            cards2 = self.cards
        
        if len(self.cards) != len(cards2):
            return False
        if self.cards_length == 1:
            return True
        elif self.cards_length == 2 or self.cards_length == 3:
            return len(uniq_rank) == 1
        elif self.cards_length == 5:
            if self.suitsIsSame(self.cards):    # tong hua / same pattern & tong hua shun
                return True
            elif self.isStraight(self.cards):   # shun / straight
                return True
            elif len(uniq_rank) == 2:           # 3 of a kind / full house & 4 of a kind
                return True
        
        return False

    def suitsIsSame(self, cards):
        first_suit = cards[0].suit
        for i in range(1, len(cards)):
            if cards[i].suit != first_suit:
                return False
        return True
    
    def isStraight(self, cards):
        for i in range(4):
            if Card.rank2val[cards[i+1].rank] != Card.rank2val[cards[i].rank] + 1:
                return False
        return True
    
    def compare(self, cards2): # compare the value between self.cards and cards2. True if self.cards > cards2, else False
        if cards2 is None:
            return True
        if self.cards_length in [1,2,3]:
            return self.compare123(cards2)
        elif self.cards_length == 5:
            return self.compare5(cards2)

    def compare123(self, cards2): # compare when card lenght = 1, 2 or 3
        cards2 = self.sort_cards(cards2)    
        if Card.rank2val[self.cards[-1].rank] == Card.rank2val[cards2[-1].rank]:
            return Card.suit2val[self.cards[-1].suit] > Card.suit2val[cards2[-1].suit]
        else:
            return Card.rank2val[self.cards[-1].rank] > Card.rank2val[cards2[-1].rank]

    def compare5(self, cards2):
        cards2 = self.sort_cards(cards2)

        c1_pattern = self.five_cards_pattern(self.cards)
        c2_pattern = self.five_cards_pattern(cards2)

        if c1_pattern[0] == c2_pattern[0]:
            if c1_pattern[0] == 4 or c1_pattern[0] == 1:    # royal flush / tong hua shun or same pattern / tong hua
                if c1_pattern[1] == c2_pattern[1]: # same suit
                    return c1_pattern[2] > c2_pattern[2] # check rank value
                else:
                    return c1_pattern[1] > c2_pattern[1] # check suit value
            if c2_pattern[0] == 3 or c2_pattern[0] == 2:    # 4 of a kind or full house / 3 of a kind
                return c1_pattern[1] > c2_pattern[1] # check rank value
            if c2_pattern[0] == 0:                          # straight / shun
                if c1_pattern[2] == c2_pattern[2]: # same rank
                    return c1_pattern[1] > c2_pattern[1] # check suit value
                else:
                    return c1_pattern[2] > c2_pattern[2] # check rank value

        else:
            return c1_pattern[0] > c2_pattern[0]

    def five_cards_pattern(self, cards):
        cards = self.sort_cards(cards)

        suit_dict = {c: Card.suit2val[c.suit] for c in cards}
        suit_counter = Counter(suit_dict.values())
        largest_suit = max(suit_counter) # suit that has largest value
        
        rank_dict = {c: Card.rank2val[c.rank] for c in cards}
        rank_counter = Counter(rank_dict.values())
        most_rank_val = max(rank_counter, key=rank_counter.get) # rank that has the most number of appearance
        largest_rank = max(rank_counter) # rank that has largest value

        # royal flush / tong hua shun
        if self.isStraight(cards) and self.suitsIsSame(cards):
            return (4, largest_suit, largest_rank)
        # 4 of a kind
        if rank_counter[most_rank_val] == 4:
            return (3, most_rank_val)
        # full house / 3 of a kind
        if rank_counter[most_rank_val] == 3:
            return (2, most_rank_val)
        # same pattern / tong hua
        elif self.suitsIsSame(cards):
            return (1, largest_suit, largest_rank)
        # straight / shun
        elif self.isStraight(cards):
            return (0, largest_suit, largest_rank)
        
class BigTwoGame:
    def __init__(self, player_names):
        self.players = [Player(name) for name in player_names]
        self.deck = Deck()
        self.distribute_cards()

    def distribute_cards(self):
        hands = self.deck.deal(len(self.players))
        # for i in range(len(self.players)):
        #     self.players[i].receive_cards(hands[i])

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
                # cur_player = self.next_player(cur_player)   # find next player
                if self.game_over():
                    self.display_winner(cur_player)
            else:
                skip_time = skip_time + 1
                # cur_player = self.next_player(cur_player)
                if skip_time > 2:
                    cur_card = None
                
            cur_player = self.next_player(cur_player)

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
        # print(f"valid: {valid}")
        # print(f"bigger: {bigger}")
        # print(f"exist: {exist}")

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