from big_two_AI_draft import Card, Hand, BigTwoGame
from availableActions import Actions
from test import Test
import re 

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
        # (Cards chosen to be played?)        
        self.action_index = action_index

# def born(self):

#     if self.done:
#         return
    
#     actions = Actions.available_actions(current_Game)
#     games = []
    
#     # Cycle through possible actions and create a list
#     # List also include the current game state
#     for i in actions:
#         new_game = self.current_Game_State
#         games.append(new_game)

#     child = {}

#     for action, game in zip(actions,games):
#         # Play the card (action) and advance the game (game)
#         game.proceed(action) # Game should be in different state after this

#         observation = game.cards
#         done = game.end
        
#         # Then create a child node
#         child = Node(game, observation, done, self, action)

#### FOR TEST_AVAILABLE_ACTIONS ####
# class game:
#     def __init__(self, cur_player_name):
#         self.cur_player = cur_player(cur_player_name)
#         self.cur_card = []

# class cur_player:
#     def __init__(self, name):
#         self.name = name
#         self.hand = []
#### FOR TEST_AVAILABLE_ACTIONS ####        

if __name__ == "__main__":
    # p1 = input("First player name: ")
    # p2 = input("Second player name: ")
    # p3 = input("Third player name: ")
    # p4 = input("Fourth player name: ")
    # players = [p1,p2,p3,p4]

    # game = BigTwoGame(players)
    # game.play_game()        

    

# Do a play, with one player as AI, choosing card randomly
    
    # Test.test_proceed_feature_in_BigTwoGame()
    
    # Test.test_filter_card_combinations()

    # A = game("TEST")
    # Test.test_available_actions(A)