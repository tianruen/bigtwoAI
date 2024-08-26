from big_two_AI_draft import Card, Hand, BigTwoGame
from availableActions import Actions
from test import Test
import random
import copy

class Node:

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

    def __init__(self, game):

        # Current game (Including actions allowed, render results etc.)
        self.game = game

    def rollout(self):
        '''
        The rollout is a random play from a copy of the environment of the current node using random moves.
        This will give us a value for the current node.
        Taken alone, this value is quite random, but, the more rollouts we will do for such node,
        the more accurate the average of the value for such node will be. This is at the core of the MCTS algorithm.
        '''
        
        # if self.done:
        #     return 100

        v = 100
        done = False
        new_game = copy.deepcopy(self.game)

        
        # Keep playing the game until a done is achieved
        while not done:
            # print()
            # print("New round, the card in node.py is: ", new_game.cur_card)
            
            if new_game.first_move:
                availableActions = Actions.available_actions(new_game)
                target_card = Card('Diamonds','3')
                action = [item for item in availableActions if target_card in item]
                # print("Action available: ")
                # for i in action:
                #     print(i)
                # TODO: Maybe to check if actions makes sense?
                action = random.choice(action)
            else:
                action = Actions.available_actions(new_game)
                # for i in action:
                #     print(i)
                # TODO: Maybe to check if actions makes sense?
                action = random.choice(action)
            #TODO: Figure out if this is a good way: We extract current player information in Actions.available_actions, without passing in any argument..?
            # print("Action played: ", action) # Only required during debugging, if finalise delete yo
            new_game.proceed(action)
            done = new_game.game_over()
            
            if done:
                winning_player = new_game.cur_player
                break

        if new_game.players.index(winning_player) == 0:                 # We are devising moves for player[0]
            v = 1
        else:
            v = 0
        
        # Now if cur_player is player[0] (me), we choose cards from "me" own hand.
        # But if cur_player is not me, we combine cards from all 3 opponents, find available moves and play them
        # Question: Would this cause problems to the game flow? (One that could now be think of is having two players finishing the same time)
        # TODO: Figure out the question (if our strategy would be problem for the game flow, or we just need some prevention mechanism)
        # Ans: Should be fine at the moment, since game_over is true if AT LEAST one player finishes, not ONLY one player finishes?

        # TODO: Can also figure out if rewards makes sense

        #TODO: Test rollout
                    
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

    result = 0
    for i in range(200):
        p1 = "Me"
        p2 = "Opp1or2or3"
        p3 = "Opp1/2/3"
        p4 = "OneOfOpp123"
        players = [p1,p2,p3,p4]

        game = BigTwoGame(players)
        game.play_game()
        
        testRollout = Node(game)
        result += testRollout.rollout()

        print(result, "/", i+1)

    

# Do a play, with one player as AI, choosing card randomly
    
    # Test.test_proceed_feature_in_BigTwoGame()
    
    # Test.test_filter_card_combinations()

    # A = game("TEST")
    # Test.test_available_actions(A)