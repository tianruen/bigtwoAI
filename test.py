from big_two_AI_draft import Card, BigTwoGame
from findingCombo import Combo
from availableActions import Actions
import re


class Test:
 
   def test_filter_card_combinations():
     
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

   def test_available_actions(game):
      
        player_hand = []
        player_hand.append(Card('Diamonds','3'))
        player_hand.append(Card('Clubs','3'))
        player_hand.append(Card('Hearts','3'))
        player_hand.append(Card('Spades','3'))
        player_hand.append(Card('Diamonds','4'))
        player_hand.append(Card('Diamonds','5'))
        player_hand.append(Card('Diamonds','6'))
        player_hand.append(Card('Clubs','6'))
        player_hand.append(Card('Diamonds','8'))
        player_hand.append(Card('Clubs','8'))
        player_hand.append(Card('Spades','8'))
        player_hand.append(Card('Hearts','J'))
        player_hand.append(Card('Spades','J'))
        player_hand.append(Card('Clubs','K'))
        game.cur_player.hand = player_hand

        cur_card = []
        cur_card.append(Card('Clubs','7'))
        cur_card.append(Card('Hearts','7'))
        cur_card.append(Card('Spades','7'))
        cur_card.append(Card('Hearts','5'))
        cur_card.append(Card('Spades','5'))
        game.cur_card = cur_card

        result = Actions.available_actions(game)

        for stuff in result:
            print(stuff)         
   
   def test_proceed_feature_in_BigTwoGame():
        p1 = "A"
        p2 = "B"
        p3 = "C"
        p4 = "D"
        players = [p1,p2,p3,p4]

        game = BigTwoGame(players)
        game.play_game()        

        while not game.game_over():
            
            print("\n")    
            print(f"{game.cur_player.name}'s turn")
            print(f"{game.cur_player.name}'s cards: {game.cur_player.hand}")
            print(f"Cards on table: {game.cur_card}")
            cards_to_play = input("Please input the card(s). Rank first then suit (e.g. 9D for 9 of Diamonds) :")
            cards_to_play = re.findall(r"([^,\s]+)", cards_to_play)

            c_list = []
            
            if cards_to_play:
                for c in cards_to_play:
                    if c[-1] == 'D':
                        s = 'Diamonds'
                    elif c[-1] == 'C':
                        s = 'Clubs'
                    elif c[-1] == 'H':
                        s = 'Hearts'
                    elif c[-1] == 'S':
                        s = 'Spades'
                    
                    if c[0] == '1':
                        r = '10'
                    else:
                        r = c[0]
                    c_list.append(Card(s,r))

            else:
                c_list.append(None)

            game.proceed(c_list)
            