from collections import defaultdict
import itertools
from big_two_AI_draft import Card, Hand

# class Node:

#     '''
#     The Node class represents a node of the MCTS tree.
#     It contains the information needed for the algorithm to run its search.
#     '''

#     def __init__(self, game, observation, done, parent, action_index):

#         # Next move / next state (Child node)
#         self.child = None

#         # Win count
#         self.T = 0

#         # Visit count
#         self.N = 0

#         # Current game (Including actions allowed, render results etc.)
#         self.game = game

#         # Observation of current game state, describing cards played?
#         self.observation = observation

#         # If game is won/loss/draw
#         self.done = done

#         # link to parent node
#         self.parent = parent

#         # index of action leading to this node 
#         # (Actions parent nodes took)        
#         self.action_index = action_index

# def born(self):

#     if self.done:
#         return
    
#     actions = []
#     games = []
    
#     # Cycle through possible actions and create a list
#     # List also include the current game state
#     for i in range(current_Game_State.available_actions):
#         actions.append(i)
#         new_game = self.current_Game_State
#         games.append(new_game)

    
#     child = {}
#     for action, game in range zip(actions,games):
#         # Play the card (action) and advance the game (game)
#         game.play(action) # Game should be in different state after this

#         observation = game.cards
#         done = game.end
        
#         # Then create a child node
#         child = Node(game, observation, done, self, action)


# def choose_action():
    
#     available_moves = []
    
#     cur_cards = game.cur_card
#     cards_length = len(cur_cards)
    
#     player_hand = game.cur_player.hand
    
#     if cards_length == 1:
#         for tobeplay_card in player_hand:
#             hand = Hand(tobeplay_card)
#             if hand.compare(cur_cards):
#                 available_moves.append(tobeplay_card)
    
#     elif cards_length == 2 or cards_length == 3:
#         combinations = filter_cards_combinations_23(player_hand, cards_length)
#         for tobeplay_cards in combinations:
#             hand = Hand(tobeplay_cards)
#             if hand.compare(cur_cards):
#                 available_moves.append(tobeplay_cards)
    
#     elif cards_length == 5:
#         ## HOW DAFUQ can we figure out all 5 cards combo..
#         # 4 of a kind:
#             # Filter out rank with 4 cards
#             # Combine it with remaining cards
        
#         # 3 of a kind:
#             # Filter out rank with 3 cards (We call this 'group rank A')
#             # Filter out rank with 2 cards (Including other rank with 3 or 4 cards except 'group rank A')
#             # Find all combination for this rank group if the rank has 3 or 4 cards
#             # Combine them

#             # Filter out rank with 4 cards (We call this 'group rank B')
#             # Find all 3 cards combination for 'group rank B'
#             # Filter out rank with 2 cards (Including other rank with 3 or 4 cards except 'group rank B')
#             # Find all combination for this rank group if the rank has 3 or 4 cards
#             # Combine them
        
#         # tonghua/tonghua shun:
#             # Combine cards based on suits
#             # Find all combination for suits with more than or equal 5 cards
        
#         # straight:
        
# def filter_cards_combinations_23(player_hand, card_length):
    
#     grouped_cards_rank = defaultdict(list)
    
#     ## Group all cards with same rank 
#     for card in player_hand:
#         r = Card.rank2val[card.rank]
#         grouped_cards_rank[r].append(card)
    
#     ## Filter away group with quantity lower than current card_length
#     ## They can't be played
#     temp_filtered_groups = [group for group in grouped_cards_rank.values() if len(group) >= card_length]
#     filtered_groups = []

#     # Find all possible combinations following card_length
#     # Using itertools.combinations
#     for group in temp_filtered_groups:
        
#         filtered_groups.extend(itertools.combinations(group, card_length))

#         # change filtered_groups from iterables to list
#         filtered_groups = [list(item) for item in filtered_groups]
    
#     return filtered_groups

def filter_cards_combinations_5(player_hand):
    
    grouped_cards_rank = defaultdict(list)
    five_card_combo = []
    
    ## Group all cards with same rank 
    for card in player_hand:
        r = Card.rank2val[card.rank]
        grouped_cards_rank[r].append(card)
    
    add_FourOfAKindCombo(grouped_cards_rank, five_card_combo)
    add_ThreeOfAKindCombo(grouped_cards_rank, five_card_combo)

    # ranks = Card.ranks

    # meal = []

    # for i in range(len(ranks) - 4):
    #     possible_straight_ranks = ranks[i:i+5]

    #     possible_meal = []
    #     for rank in possible_straight_ranks:
    #         if grouped_cards_rank[rank]:
    #             possible_meal.append(grouped_cards_rank[rank])
    #         else:
    #             break
    
    #     if len(possible_meal) == 5:
    #         meal.extend(itertools.product(*possible_meal))
    #         meal = [list(item) for item in meal]
    #         five_card_combo.append(meal)

    
    return five_card_combo

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
            meal.append(liao)                    # Can't do extend because liao is single Card object, not iterable list of Card object(?)
            five_card_combo.append(meal)

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
            five_card_combo.append(meal)

if __name__ == "__main__":
    # p1 = input("First player name: ")
    # p2 = input("Second player name: ")
    # p3 = input("Third player name: ")
    # p4 = input("Fourth player name: ")
    # players = [p1,p2,p3,p4]

    # game = BigTwoGame(players)
    # game.play_game()        

# Do a play, with one player as AI, choosing card randomly



    #### TESTING FOR FILTER_CARDS_COMBINATIONS : 2 and 3 cards####
    
    player_hand = []
    player_hand.append(Card('Diamonds','3'))
    player_hand.append(Card('Clubs','3'))
    player_hand.append(Card('Hearts','3'))
    player_hand.append(Card('Spades','3'))
    player_hand.append(Card('Diamonds','4'))
    player_hand.append(Card('Spades','5'))
    player_hand.append(Card('Diamonds','6'))
    player_hand.append(Card('Clubs','6'))
    player_hand.append(Card('Hearts','7'))
    player_hand.append(Card('Spades','8'))
    player_hand.append(Card('Diamonds','J'))
    player_hand.append(Card('Clubs','J'))
    player_hand.append(Card('Hearts','J'))
    player_hand.append(Card('Spades','J'))

    result = filter_cards_combinations_5(player_hand)

    for stuff in result:
        print (stuff)

    #### TESTING FOR FILTER_CARDS_COMBINATIONS : 2 and 3 cards ####
