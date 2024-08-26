from big_two_AI_draft import Hand
from findingCombo import Combo

class Actions:

    def available_actions(game):
           
        available_actions = []

        cur_cards = game.cur_card

        if game.players.index(game.cur_player) == 0:
            playing_hand = game.cur_player.hand
        else:
            playing_hand = game.players[1].hand.copy()
            playing_hand.extend(game.players[2].hand)
            playing_hand.extend(game.players[3].hand)       # We focus on devising moves for player[0]

        if not cur_cards:
            available_actions.extend([[card] for card in playing_hand])                         # Add possible Single plays
            available_actions.extend(Combo.filter_cards_combinations_23(playing_hand, 2))       # Add possible Double plays
            available_actions.extend(Combo.filter_cards_combinations_23(playing_hand, 3))       # Add possible Triple plays
            available_actions.extend(Combo.filter_cards_combinations_5(playing_hand))           # Add possible Five Cards combo
        else:
            cards_length = len(cur_cards)

            if cards_length == 1:
                available_actions = findSingle(playing_hand, cur_cards)
            elif cards_length == 2:
                available_actions = findDouble(playing_hand, cur_cards)
            elif cards_length == 3:
                available_actions = findTriple(playing_hand, cur_cards)
            elif cards_length == 5:
                available_actions = findFiveCardsCombo(playing_hand, cur_cards)
        
        if not game.first_move:
            available_actions.append(None)        # Avoid playing skip in the first move of the game
        
        return available_actions
    



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

        