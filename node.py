from collections import defaultdict
import itertools
from big_two_AI_draft import Card, Hand

class Node:

    '''
    The Node class represents a node of the MCTS tree.
    It contains the information needed for the algorithm to run its search.
    '''

    def __init__(self, game, observation, done, parent, action_index):

        # Next move / next state (Child node)
        self.child = None

        # Win count
        self.T = 0

        # Visit count
        self.N = 0

        # Current game (Including actions allowed, render results etc.)
        self.game = game

        # Observation of current game state, describing cards played?
        self.observation = observation

        # If game is won/loss/draw
        self.done = done

        # link to parent node
        self.parent = parent

        # index of action leading to this node 
        # (Actions parent nodes took)        
        self.action_index = action_index

def born(self):

    if self.done:
        return
    
    actions = []
    games = []
    
    # Cycle through possible actions and create a list
    # List also include the current game state
    for i in range(current_Game_State.available_actions):
        actions.append(i)
        new_game = self.current_Game_State
        games.append(new_game)

    
    child = {}
    for action, game in range zip(actions,games):
        # Play the card (action) and advance the game (game)
        game.play(action) # Game should be in different state after this

        observation = game.cards
        done = game.end
        
        # Then create a child node
        child = Node(game, observation, done, self, action)


def choose_action():
    
    available_moves = []
    
    cur_cards = game.cur_card
    cards_length = len(cur_cards)
    
    player_hand = game.cur_player.hand
    
    if cards_length == 1:
        for tobeplay_card in player_hand:
            hand = Hand(tobeplay_card)
            if hand.compare(cur_cards):
                available_moves.append(tobeplay_card)
    
    elif cards_length == 2 or cards_length == 3:
        combinations = filter_cards_combinations_23(player_hand, cards_length)
        for tobeplay_cards in combinations:
            hand = Hand(tobeplay_cards)
            if hand.compare(cur_cards):
                available_moves.append(tobeplay_cards)
    
    elif cards_length == 5:
        ## HOW DAFUQ can we figure out all 5 cards combo..
        # 4 of a kind:
            # Filter out rank with 4 cards
            # Combine it with remaining cards
        
        # 3 of a kind:
            # Filter out rank with 3 cards (We call this 'group rank A')
            # Filter out rank with 2 cards (Including other rank with 3 or 4 cards except 'group rank A')
            # Find all combination for this rank group if the rank has 3 or 4 cards
            # Combine them

            # Filter out rank with 4 cards (We call this 'group rank B')
            # Find all 3 cards combination for 'group rank B'
            # Filter out rank with 2 cards (Including other rank with 3 or 4 cards except 'group rank B')
            # Find all combination for this rank group if the rank has 3 or 4 cards
            # Combine them
        
        # tonghua/tonghua shun:
            # Combine cards based on suits
            # Find all combination for suits with more than or equal 5 cards
        
        # straight:
        
def filter_cards_combinations_23(player_hand, card_length):
    
    grouped_cards = defaultdict(list)
    
    ## Group all cards with same rank 
    for card in player_hand:
        r = Card.rank2val[card.rank]
        grouped_cards[r].append(card)
    
    ## Filter away group with quantity lower than current card_length
    ## They can't be played
    temp_filtered_groups = [group for group in grouped_cards.values() if len(group) >= card_length]
    filtered_groups = []

    for group in temp_filtered_groups:
        
        ## Just include the group if they have the same quantity as current card_length
        
        ### TODO: Test if this line is needed or cover in next condition , changing > to >=?
        if len(group) == card_length:
            filtered_groups.append(group)
        
        
        # If a rank has more cards than card_length, 
        # consider all case
        # Example: card_length is 2, but we have 3D, 3C, 3H
        # We include all combinations into filtered_groups
        
        elif len(group) > card_length:

            ### TODO: Test if we can straight change combinations to filtered_group?
            combinations = list(itertools.combinations(group, card_length))
            
            ### Uncomment line below if want to change tuple item to list
            # combinations = [list(item) for item in combinations]
            
            for combo in combinations:
                filtered_groups.append(combo)
    
    return filtered_groups

def filter_cards_combinations_5(player_hand):
    
    grouped_cards_rank = defaultdict(list)
    five_card_combo = []
    
    ## Group all cards with same rank 
    for card in player_hand:
        r = Card.rank2val[card.rank]
        grouped_cards_rank[r].append(card)
    

    # 4 of a kind
    dish = [group for group in grouped_cards_rank.values() if len(group) == 4]
    
    for food in dish:
        sauce = grouped_cards_rank
        sauce.remove(food)

        for liao in sauce:
            meal = food
            meal.extend(liao)
            five_card_combo.append(meal)

    # 3 of a kind
    temp_dish = [group for group in grouped_cards_rank.values() if len(group) >= 3]
    dish = []

    for plate in temp_dish:
        if len(plate) == 3:
            dish.append(plate)
        elif len(plate) > 3:
            combinations = list(itertools.combinations(plate, 3))
            for combo in combinations:
                dish.append(combo)
    
    for food in dish:
        temp_sauce = [group for group in grouped_cards_rank.values() if len(group) >= 2]
        temp_sauce.remove(food[r])
        sauce = []

        for bowl in temp_sauce:
            if len(bowl) == 2:
                sauce.append(bowl)
            elif len(bowl) > 2:
                combinations = list(itertools.combinations(bowl, 2))
                for combo in combinations:
                    sauce.append(combo)
        
        for liao in sauce:
            meal = food
            meal.extend(liao)
            five_card_combo.append(meal)
            

if __name__ == "__main__":
    p1 = input("First player name: ")
    p2 = input("Second player name: ")
    p3 = input("Third player name: ")
    p4 = input("Fourth player name: ")
    players = [p1,p2,p3,p4]

    game = BigTwoGame(players)
    game.play_game()        

# Do a play, with one player as AI, choosing card randomly



    #### TESTING FOR FILTER_CARDS_COMBINATIONS : 2 and 3 cards####
    
    # player_hand = []
    # player_hand.append(Card('Diamonds','3'))
    # player_hand.append(Card('Clubs','3'))
    # player_hand.append(Card('Hearts','3'))
    # player_hand.append(Card('Diamonds','4'))
    # player_hand.append(Card('Spades','5'))
    # player_hand.append(Card('Diamonds','6'))
    # player_hand.append(Card('Clubs','6'))
    # player_hand.append(Card('Hearts','6'))
    # player_hand.append(Card('Spades','6'))

    # result = filter_cards_combinations(player_hand, 3)

    # print(result)

    #### TESTING FOR FILTER_CARDS_COMBINATIONS : 2 and 3 cards ####
