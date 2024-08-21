from big_two_AI_draft import Card, Hand, BigTwoGame
from availableActions import Actions
from test import Test
import re 

# class Node:

#     '''
#     The Node class represents a node of the MCTS tree.
#     It contains the information needed for the algorithm to run its search.
#     '''

#     def __init__(self, game, done, parent, action_index):

#         # Next move / next state (Child node)
#         self.child = None

#         # Win count
#         self.T = 0

#         # Visit count
#         self.N = 0

#         # Current game (Including actions allowed, render results etc.)
#         self.game = game

#         # Observation of current game state, describing cards played?
#         # self.observation = observation

#         # If game is won/loss/draw
#         self.done = done

#         # link to parent node
#         self.parent = parent

#         # index of action leading to this node 
#         # (Actions parent nodes took)
#         # (Cards chosen to be played?)        
#         self.action_index = action_index

#     def born(self, current_game):

#         if self.done:
#             # Do the reward things?
#             return

#         actions = Actions.available_actions(current_game)
#         games = []

#         # Cycle through possible actions and create a list
#         # List also include the current game state
#         for i in actions:
#             new_game = current_game
#             games.append(new_game)

#         child = {}

#         for action, game in zip(actions,games):
#             # Play the card (action) and advance the game (game)
#             game.proceed(action) # Game should be in different state after this

#             done = game.game_over()
            
#             # Then create a child node
#             child = Node(game, done, self, action)

#     def explore(self):
#         '''
#         The search along the tree is as follows:
#         - from the current node, recursively pick the children which maximizes the value according to the MCTS formula
#         - when a leaf is reached:
#             - if it has never been explored before, do a rollout and update its current value
#             - otherwise, expand the node creating its children, pick one child at random, do a rollout and update its value
#         - backpropagate the updated statistics up the tree until the root: update both value and visit counts
#         '''
#         ### The game started with a lot of exploring...
#         current = self

#         # If the node is explored before, thus got children..
#         while current.child:

#             # Enter into child node (We named the child node A)
#             child = current.child

#             ## Search for highest UCB score in whole of A's child nodes?
#             max_U = max(c.getUCBscore() for c in child.values())

#             # Creates a list that includes all actions from A's child that has highest UCB score
#             actions = [a for a,c in child.items() if c.getUCBscore() == max_U]

#             # Pick a random action from the list
#             action = randomly choose available actions

#             # Enter into A's child node?
#             current = child[action]
        
#         # If first time visiting a node
#         if current.N < 1:
#             # Do rollout and calculate win rate?
#             current.T = current.T + current.rollout()
        
#         # Carry out this if is a leaf node and hasn't been visited
#         else:
#             # Create child nodes
#             current.born()

#             if current.child:
#                 # Enter a random child's node
#                 current = random.choice(current.child)

#             # Do rollout and calculate win rate
#             current.T = current.T + current.rollout()
        
#         # Increase visit count
#         current.N += 1

#         ## This part does update statistics and backpropagate
#         parent = current

#         while parent.parent:
#             parent = parent.parent
#             parent.N += 1
#             parent.T = parent.T + current.T

    def rollout(self):
        '''
        The rollout is a random play from a copy of the environment of the current node using random moves.
        This will give us a value for the current node.
        Taken alone, this value is quite random, but, the more rollouts we will do for such node,
        the more accurate the average of the value for such node will be. This is at the core of the MCTS algorithm.
        '''
                
        if self.done:
            return 0

        v = 0
        done = False
        new_game = self.game.copy()

        
        # Keep playing the game until a done is achieved
        while not done:
            action = Actions.available_actions(new_game).random
            #TODO: Check if syntax is correct
            #TODO: Figure out if this is a good way: We extract current player information in Actions.available_actions, without passing in any argument..?


            new_game.proceed(action)
            done = new_game.game_over()
            # need to figure out how to set out reward
            # probably at the end of the game then give 1 if won?
            
            if done:
                break

        if winning player = me:
            v = 1
        else:
            v = 0
            
        return v
    

    


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