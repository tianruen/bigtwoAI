from big_two_AI_draft import Card, Hand
from findingCombo import Combo

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



if __name__ == "__main__":
    # p1 = input("First player name: ")
    # p2 = input("Second player name: ")
    # p3 = input("Third player name: ")
    # p4 = input("Fourth player name: ")
    # players = [p1,p2,p3,p4]

    # game = BigTwoGame(players)
    # game.play_game()        

# Do a play, with one player as AI, choosing card randomly



    #### TESTING FOR FILTER_CARDS_COMBINATIONS####
    
    player_hand = []
    player_hand.append(Card('Diamonds','3'))
    player_hand.append(Card('Clubs','3'))
    player_hand.append(Card('Hearts','3'))
    player_hand.append(Card('Spades','3'))
    player_hand.append(Card('Diamonds','4'))
    player_hand.append(Card('Diamonds','5'))
    player_hand.append(Card('Diamonds','6'))
    player_hand.append(Card('Clubs','6'))
    player_hand.append(Card('Diamonds','7'))
    player_hand.append(Card('Spades','8'))
    player_hand.append(Card('Diamonds', '9'))
    player_hand.append(Card('Diamonds','J'))
    player_hand.append(Card('Clubs','J'))
    player_hand.append(Card('Hearts','J'))
    player_hand.append(Card('Spades','J'))
    player_hand.append(Card('Diamonds','Q'))
    player_hand.append(Card('Clubs','K'))
    player_hand.append(Card('Diamonds','A'))
    player_hand.append(Card('Clubs','A'))
    player_hand.append(Card('Hearts','A'))
    player_hand.append(Card('Spades','A'))
    player_hand.append(Card('Spades', '2'))

    result2 = Combo.filter_cards_combinations_23(player_hand,2)
    result3 = Combo.filter_cards_combinations_23(player_hand,3)
    result5 = Combo.filter_cards_combinations_5(player_hand)

    result = []
    result.extend(result2)
    result.extend(result3)
    result.extend(result5)

    for stuff in result:
        print(stuff)
    
    #### TESTING FOR FILTER_CARDS_COMBINATIONS####
