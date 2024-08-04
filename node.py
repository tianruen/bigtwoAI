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

