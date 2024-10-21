import random
from collections import Counter, defaultdict
import itertools
import re
from typing import List, Tuple

# import availableActions
# import findingCombo

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
    def __init__(self, name:str, type_:str):
        self.name = name
        self.hand = []
        self.type = type_
        
    def __repr__(self):
        return f"{self.name}: {self.hand}"

    def receive_cards(self, cards):
        self.hand.extend(cards)
        self.hand.sort()

    def play_cards(self, cards):
        for card in cards:
            self.hand.remove(card)

    def get_available_actions(self, table_cards:List[List[Card]]):
        first_round = []
        if table_cards is not None:
            cards_length = len(table_cards)
            if cards_length == 1:
                available_actions = findSingle(self.hand, table_cards)
            elif cards_length == 2:
                available_actions = findDouble(self.hand, table_cards)
            elif cards_length == 3:
                available_actions = findTriple(self.hand, table_cards)
            elif cards_length == 5:
                available_actions = findFiveCardsCombo(self.hand, table_cards)
            available_actions.append(None)
        else:
            available_actions = []
            available_actions.extend([[card] for card in self.hand])                         # Add possible Single plays
            available_actions.extend(Combo.filter_cards_combinations_23(self.hand, 2))       # Add possible Double plays
            available_actions.extend(Combo.filter_cards_combinations_23(self.hand, 3))       # Add possible Triple plays
            available_actions.extend(Combo.filter_cards_combinations_5(self.hand))           # Add possible Five Cards combo
            first_round = [act for act in available_actions if Card("Diamonds", "3") in act]
        return first_round if first_round else available_actions
    # available_actions if [Card("Diamonds", "3")] not in available_actions else first_round
        # return available_actions if [Card("Diamonds", "3")] not in available_actions else first_round
    
    def get_action(self, available_actions:List[List[Card]]):
        # replace with other strategies in the future
        return random.choice(available_actions)
    
class Hand:
    def __init__(self, cards:List[Card]):
        self.cards = cards
        self.cards.sort()
        self.cards_length = len(self.cards)
        
    def is_valid(self, cards2:List[Card]=None):
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
            next_rank = c.ranks[(c.ranks.index(c.rank) + 1) % 13]
            if next_rank != cards[i+1].rank:
                return False
        return True
    
    def compare(self, cards2:List[Card]=None): # compare the value between self.cards and cards2. True if self.cards > cards2, else False
        if cards2 is None or len(cards2) == 0:
            return True
        cards2.sort()
        if self.cards_length in [1, 2, 3]:  # for single, double, and triple
            return self.cards[-1] > cards2[-1]
        elif self.cards_length == 5:
            return self.compare5(cards2)
        return False
        
    def compare5(self, cards2):
        cards2.sort()
        
        c1_pattern = self.five_cards_pattern(self.cards)
        c2_pattern = self.five_cards_pattern(cards2)
        
        if c1_pattern[0] == c2_pattern[0]:
            if c1_pattern[0] == 0:          # straight
                return c1_pattern[1] > c2_pattern[1]
            if c1_pattern[0] in [1,4]:    # royal flush/tong hua shun or same pattern/tong hua or straight
                if c1_pattern[1].suit == c2_pattern[1].suit:    # same suit
                    return c1_pattern[1] > c2_pattern[1]        # check rank value
                else:
                    return Card.suits.index(c1_pattern[1].suit) > Card.suits.index(c2_pattern[1].suit)    # check suit value
            if c2_pattern[0] in [2,3]:    # 4 of a kind or full house/3 of a kind
                return Card.ranks.index(c1_pattern[1]) > Card.ranks.index(c2_pattern[1]) # check rank value
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
        if max(rank_counter.values()) == 4:
            return (3, most_repeated_rank)
        # full house / 3 of a kind
        if max(rank_counter.values()) == 3:
            return (2, most_repeated_rank)
        # same pattern / tong hua
        if self.suitsIsSame(cards):
            return (1, max(cards))
        # straight / shun
        if self.isStraight(cards):
            return (0, max(cards))

class Combo:
    
    ############ DOUBLE or TRIPLE ############
    def filter_cards_combinations_23(playing_hand, card_length):
        
        grouped_cards_rank = defaultdict(list)
        
        ## Group all cards with same rank 
        for card in playing_hand:
            r = card.rank
            grouped_cards_rank[r].append(card)
        
        ## Filter away group with quantity lower than current card_length
        ## They can't be played
        temp_filtered_groups = [group for group in grouped_cards_rank.values() if len(group) >= card_length]
        filtered_groups = []

        # Find all possible combinations following card_length
        # Using itertools.combinations
        for group in temp_filtered_groups:
            
            filtered_groups.extend(itertools.combinations(group, card_length))

        # change filtered_groups from iterables to list
        filtered_groups = [list(item) for item in filtered_groups]
        
        return filtered_groups

    
    ############ FIVE CARDS ############
    def filter_cards_combinations_5(playing_hand):
        
        grouped_cards_rank = defaultdict(list)
        grouped_cards_suit = defaultdict(list)
        five_card_combo = []
        
        ## Group all cards with same rank 
        for card in playing_hand:
            r = card.rank
            grouped_cards_rank[r].append(card)

        for card in playing_hand:
            s = card.suit
            grouped_cards_suit[s].append(card)
        
        add_FourOfAKindCombo(grouped_cards_rank, five_card_combo)
        add_ThreeOfAKindCombo(grouped_cards_rank, five_card_combo)
        add_Flush(grouped_cards_suit, five_card_combo)
        add_Straight(grouped_cards_rank, five_card_combo)

        # There might be repetition of combinations:
        # Royal flush might be included twice from add_Flush and add_Straight
        # We remove duplicates!
        five_card_combo = list(dict.fromkeys(tuple(item) for item in five_card_combo))
        five_card_combo = [list(item) for item in five_card_combo]    # Is this necessary? (Changing all elements from tuple(?) to list)

        return five_card_combo

#################################################################
######### METHODS ASSISTING FILTER_CARDS_COMBINATIONS_5 #########
#################################################################
#####
    # Those are:
    #   add_FourOfAKindCombo
    #   add_ThreeOfAKindCombo
    #   add_Flush
    #   add_Straight
#####

def add_FourOfAKindCombo(grouped_cards_rank, five_card_combo):
    # 4 of a kind , LETS GO
    
    # grouped_cards_rank is a dictionary with ranks as key and the value are all the cards with the rank
    # find groups that has at least four cards
    # Name these groups DISH
    dish = [group for group in grouped_cards_rank.values() if len(group) == 4]

    for food in dish:
        sauce = grouped_cards_rank.copy()

        # Exclude group of the chosen rank
        # Then sauce.remove(food)
        # But dict doesn't allow it to be easy, so we do following
        # Shit
        for key, value in sauce.items():
            if value == food:
                del sauce[key]
                break

        # Now we transform sauce from dict to list
        # Without key(rank)
        # SAUCE is now single cards to be paired with DISH
        sauce = [item for value_list in sauce.values() for item in value_list]

        # PAIR THE SHIT OUT OF THEM, AND MAKE A FKING MEAL
        for liao in sauce:
            meal = food.copy()
            meal.append(liao)                   # Can't do extend because liao is single Card object, not iterable list of Card object(?)
            five_card_combo.append(meal)        # five_card_combo is not returned because the five_card_combo passed in is a list
                                                # It is iterable, thus it is original
                                                # Meaning changing five_card_combo here also directly modify original five_card_combo

def add_ThreeOfAKindCombo(grouped_cards_rank, five_card_combo):
    # 3 of a kind , LETS GO

    # grouped_cards_rank is a dictionary with ranks as key and the value are all the cards with the rank
    # find groups that has at least three cards
    # Name these groups TEMP_DISH, because we are going to do some combo
    temp_dish = [group for group in grouped_cards_rank.values() if len(group) >= 3]
    dish = []

    # TEMP_DISH goes through combo
    # and we have fucking dishes
    # group DISH contains all possible 3 card combinations
    for plate in temp_dish:
        dish.extend(itertools.combinations(plate, 3))
    dish = [list(item) for item in dish]
    
    for food in dish:
        temp_sauce = grouped_cards_rank.copy()

        # Exclude group of the chosen rank
        # Concept is like temp_sauce.remove(food)
        for key, value in temp_sauce.items():
            if all(item in value for item in food):
                del temp_sauce[key]
                break
        # TEMP_SAUCE group now contains all the group except chosen rank group

        # Find groups that has at least two cards
        # At the same time we transform TEMP_SAUCE from dict to list
        temp_sauce = [group for group in temp_sauce.values() if len(group) >= 2]
        
        sauce = []

        # TEMP_SAUCE goes through combo
        # and we have fucking sauces
        # group SAUCE contains all possible 2 card combinations
        for bowl in temp_sauce:
            sauce.extend(itertools.combinations(bowl, 2))
        sauce = [list(item) for item in sauce]
        
        # PAIR THE SHIT OUT OF THEM, AND MAKE A FKING MEAL
        for liao in sauce:
            meal = food.copy()
            meal.extend(liao)                   # Can't do append because it creates list within list
            five_card_combo.append(meal)        # five_card_combo is not returned because the five_card_combo passed in is a list
                                                # It is iterable, thus it is original
                                                # Meaning changing five_card_combo here also directly modify original five_card_combo

def add_Flush(grouped_cards_suit, five_card_combo):
    temp_meal = [group for group in grouped_cards_suit.values() if len(group) >= 5]
    meal = []

    for course in temp_meal:
        meal.extend(itertools.combinations(course, 5))
    meal = [list(item) for item in meal]
    
    five_card_combo.extend(meal)                # five_card_combo is not returned because the five_card_combo passed in is a list
                                                # It is iterable, thus it is original
                                                # Meaning changing five_card_combo here also directly modify original five_card_combo

def add_Straight(grouped_cards_rank, five_card_combo):
    # Straights, LETS GO

    # Create ranks that would be used as reference later
    ranks = Card.ranks
    meal = []

    # From 3-7 until J-2
    for i in range(len(ranks) - 4):
        
        # This is the reference
        possible_straight_ranks = ranks[i:i+5]
        possible_meal = []

        for rank in possible_straight_ranks:
            
            # If we found the rank contains card
            # we include it into POSSIBLE_MEAL
            if grouped_cards_rank[rank]:
                possible_meal.append(grouped_cards_rank[rank])
            # AND we gg if it didn't find
            else:
                break
    
        # POSSIBLE_MEAL will contain five cards
        # if there is five cards
        if len(possible_meal) == 5:

            # And we find all combinations to form the straight
            # E.g. 3-7 but we have 3 diamonds and 3 clubs
            # And we have a MEAL!
            meal.extend(itertools.product(*possible_meal))
            
    # Transform all collected MEALs from iterable to list!
    meal = [list(item) for item in meal]

    # AND SERVE THOSE FKING MEALS
    five_card_combo.extend(meal)                # five_card_combo is not returned because the five_card_combo passed in is a list
                                                # It is iterable, thus it is original
                                                # Meaning changing five_card_combo here also directly modify original five_card_combo


#################################################################
######### METHODS ASSISTING FILTER_CARDS_COMBINATIONS_5 #########
#################################################################

# class Actions:

#     def available_actions(game):
           
#         available_actions = []

#         cur_cards = game.cur_card

#         if game.players.index(game.cur_player) == 0:
#             playing_hand = game.cur_player.hand
#         else:
#             playing_hand = game.players[1].hand.copy()
#             playing_hand.extend(game.players[2].hand)
#             playing_hand.extend(game.players[3].hand)       # We focus on devising moves for player[0]

#         if not cur_cards:
#             available_actions.extend([[card] for card in playing_hand])                         # Add possible Single plays
#             available_actions.extend(Combo.filter_cards_combinations_23(playing_hand, 2))       # Add possible Double plays
#             available_actions.extend(Combo.filter_cards_combinations_23(playing_hand, 3))       # Add possible Triple plays
#             available_actions.extend(Combo.filter_cards_combinations_5(playing_hand))           # Add possible Five Cards combo
#         else:
#             cards_length = len(cur_cards)

#             if cards_length == 1:
#                 available_actions = findSingle(playing_hand, cur_cards)
#             elif cards_length == 2:
#                 available_actions = findDouble(playing_hand, cur_cards)
#             elif cards_length == 3:
#                 available_actions = findTriple(playing_hand, cur_cards)
#             elif cards_length == 5:
#                 available_actions = findFiveCardsCombo(playing_hand, cur_cards)
        
#         if not game.first_move:
#             available_actions.append(None)        # Avoid playing skip in the first move of the game
        
#         return available_actions

#################################################################
######### METHODS ASSISTING AVAILABLE_ACTIONS #########
#################################################################
#####
    # Those are:
    #   findSingle
    #   findDouble
    #   findTriple
    #   findFiveCardsCombo
#####

def findSingle(playing_hand, cur_cards):
    available_moves = []
    for tobeplay_card in playing_hand:
        hand = []
        hand.append(tobeplay_card)
        hand = Hand(hand)                   # Would have error of Card not is not an iterable if we do "hand = Hand(tobeplay_card)" directly
        if hand.compare(cur_cards):
            available_moves.append([tobeplay_card])
    
    return available_moves

def findDouble(playing_hand, cur_cards):
    available_moves = []
    combinations = Combo.filter_cards_combinations_23(playing_hand, 2)
    for tobeplay_cards in combinations:
        hand = Hand(tobeplay_cards)
        if hand.compare(cur_cards):
            available_moves.append(tobeplay_cards)

    return available_moves

def findTriple(playing_hand, cur_cards):
    available_moves = []
    combinations = Combo.filter_cards_combinations_23(playing_hand, 3)
    for tobeplay_cards in combinations:
        hand = Hand(tobeplay_cards)
        if hand.compare(cur_cards):
            available_moves.append(tobeplay_cards)

    return available_moves

def findFiveCardsCombo(playing_hand, cur_cards):
    available_moves = []
    combinations = Combo.filter_cards_combinations_5(playing_hand)
    for tobeplay_combo in combinations:
        hand = Hand(tobeplay_combo)
        if hand.compare(cur_cards):
            available_moves.append(tobeplay_combo)

    return available_moves

#################################################################
######### METHODS ASSISTING AVAILABLE_ACTIONS #########
#################################################################

class BigTwoGame:
    def __init__(self, player_names_types:List[Tuple[str,str]]):
        self.players = [Player(n, t) for n, t in player_names_types]
        self.deck = Deck()
        self.distribute_cards()
        self.starting_player()
        self.game_hist = []
        
    def distribute_cards(self):
        hands = self.deck.deal(len(self.players))
        for player, hand in zip(self.players, hands):
            player.receive_cards(hand)
            
    def starting_player(self, start_type='3D'):
        assert start_type in ['3D', 'winner']
        if start_type == '3D':
            for player in self.players:
                for card in player.hand:
                    if card.suit == 'Diamonds' and card.rank == '3':
                        self.cur_player = player
        elif start_type == 'winner':
            pass
            # TODO: implement the winner starting player
        
    def next_player(self, cur_player):
        cur_index = self.players.index(cur_player)
        return self.players[(cur_index + 1) % len(self.players)]
    
    def play_turn(self, play_cards:List[Card]):    
        if play_cards is not None:
            table_cards = next((p_c[1] for p_c in self.game_hist[-3:][::-1] if p_c[1] is not None), None)   # p_c: (player, played_cards)
            # check if the move is valid
            # assert all([c in self.cur_player.hand for c in play_cards])
            hand = Hand(play_cards)
            assert hand.is_valid(table_cards)
            assert hand.compare(table_cards)
            # execute action
            self.cur_player.play_cards(play_cards)
            # print(f"{self.cur_player.name} played: {play_cards}")
        # elif play_cards is None:
        #     print(f"{self.cur_player.name} skipped")
        
        self.game_hist.append((self.cur_player.name, play_cards))
        self.cur_player = self.next_player(self.cur_player)
    
    def game_over(self):
        return any([len(player.hand) == 0 for player in self.players])
    
    def display_winner(self):
        for player in self.players:
            if len(player.hand) == 0:
                winner = player.name
                self.winner = player
        print(f"{winner} is the winner")

if __name__ == "__main__":
    # p1 = input("First player name: ")
    # p2 = input("Second player name: ")
    # p3 = input("Third player name: ")
    # p4 = input("Fourth player name: ")
    # random.seed(42)
    win_rate = [0 for _ in range(4)]
    n = 50
    for i in range(n):
        random_state = random.getstate()
        random.setstate(random_state)
        
        p1, p2, p3, p4 = "A", "B1", "B2", "B3"
        t1, t2, t3, t4 = "Agent", "Bot", "Bot", "Bot"
        p_t = zip([p1,p2,p3,p4], [t1,t2,t3,t4])
        # players = [p1,p2,p3,p4]
        
        game = BigTwoGame(p_t)
        while not game.game_over():
            cur_player = game.cur_player
            table_card = next((p_c[1] for p_c in game.game_hist[-3:][::-1] if p_c[1] is not None), None)
            
            avail_act = cur_player.get_available_actions(table_card)
            action = cur_player.get_action(avail_act)
            
            # print(cur_player.name)
            # print(f"Available action: {avail_act}")
            # print(f"Played: {action}")
            
            game.play_turn(action)
        # game.display_winner()
        
        winner_idx = [len(player.hand) == 0 for player in game.players].index(True)
        win_rate[winner_idx] += 1
        
        # print(i)
        print([wr/(i+1) for wr in win_rate])