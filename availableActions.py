from big_two_AI_draft import Hand
from findingCombo import Combo

class Actions:

    def available_actions(game):
        
        available_moves = []
        
        cur_cards = game.cur_card
        cards_length = len(cur_cards)

        player_hand = game.cur_player.hand
        
        if cards_length == 1:
            for tobeplay_card in player_hand:
                hand = []
                hand.append(tobeplay_card)
                hand = Hand(hand)                   # Would have error of Card not is not an iterable if we do "hand = Hand(tobeplay_card)" directly
                if hand.compare(cur_cards):
                    available_moves.append(tobeplay_card)
        
        elif cards_length == 2 or cards_length == 3:
            combinations = Combo.filter_cards_combinations_23(player_hand, cards_length)
            for tobeplay_cards in combinations:
                hand = Hand(tobeplay_cards)
                if hand.compare(cur_cards):
                    available_moves.append(tobeplay_cards)
        
        elif cards_length == 5:
            combinations = Combo.filter_cards_combinations_5(player_hand)
            for tobeplay_combo in combinations:
                hand = Hand(tobeplay_combo)
                if hand.compare(cur_cards):
                    available_moves.append(tobeplay_combo)

        return available_moves