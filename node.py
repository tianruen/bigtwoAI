from collections import defaultdict
import itertools

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
    
    elif card_length == 2 or card_length == 3:
    
        combinations = filter_cards_combinations(player_hand, card_length)
        for tobeplay_combo in combinations:
            hand = Hand(tobeplay_combo)
            if hand.compare(cur_cards):
                available_moves.append(tobeplay_combo)
        
        
def filter_cards_combinations(player_hand, card_length):
    
    grouped_cards = defaultdict(list)
    
    ## Group all cards with same rank 
    for card in player_hand:
        r = Card.rank2val[card.rank]
        grouped_cards[r].append(card)
    
    ## Filter away group with quantity lower than current card_length
    ## They can't be played
    temp_filtered_groups = [group for group in grouped_cards.values() if len(group) >= card_length)
    filtered_groups = []
    
    for group in temp_filtered_groups:
        
        ## Just include the group if they have the same quantity as current card_length
        if len(group) == card_length:
            filtered_groups.append(group)
        
        
        # If a rank has more cards than card_length, 
        # consider all case
        # Example: card_length is 2, but we have 3D, 3C, 3H
        # We include all combinations into filtered_cards_combo
        
        elif len(group) > card_length:
            combinations = list(itertools.combinations(group, card_length)
            for combo in combinations:
                fitlered_cards_combo.append(combo)
    
    
    return filtered_cards_combo

if __name__ == "__main__":
    p1 = input("First player name: ")
    p2 = input("Second player name: ")
    p3 = input("Third player name: ")
    p4 = input("Fourth player name: ")
    players = [p1,p2,p3,p4]

    game = BigTwoGame(players)
    game.play_game()        

# Do a play, with one player as AI, choosing card randomly