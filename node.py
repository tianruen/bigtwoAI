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


def choose_action(card_length):
    
    game.cur_player.hand = game.cur_player.hand.sort_cards(game.cur_player.hand.cards)
    
    available_moves = []
    cur_hand = game.cur_player.hand
    
    
    if card_length == 1:
        cur_card_rank = Card.rank2val[game.cur_card.rank]
        cur_card_suit = Card.suit2val[game.cur_card.suit]
        
        for i in cur_hand:
            r = Card.rank2val[i.rank]
            if r > cur_card_rank:
                available_moves.append(i)       # This includes the card that can be played... is this a good way?
            
            elif r = cur_card_rank:
                s = Card.suit2val[i.suit]
                if s > cur_card_suit:
                    available_moves.append(i)   # This includes the card that can be played... is this a good way?
    
    elif card_length == 2:
    
        ###After compare rank, compare smallest suit?
        
    elif card_length == 3:
        ###Just compare suit
        
        ###Take inspiration fromm compare123, compare5
        

if __name__ == "__main__":
    p1 = input("First player name: ")
    p2 = input("Second player name: ")
    p3 = input("Third player name: ")
    p4 = input("Fourth player name: ")
    players = [p1,p2,p3,p4]

    game = BigTwoGame(players)
    game.play_game()        

# Do a play, with one player as AI, choosing card randomly