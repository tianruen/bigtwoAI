from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.scrollview import ScrollView
from kivy.uix.behaviors import ButtonBehavior

from big_two_draft1 import *


class imgbtn(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(imgbtn, self).__init__(**kwargs)

    def on_press(self):
        print("Button pressed", self.source)
        CardDeckApp.l1.text = self.source

class lblbtn(ButtonBehavior, Label):
    def __init__(self, **kwargs):
        super(lblbtn, self).__init__(**kwargs)

    def on_press(self):
        print("Button pressed", self.text)
        CardDeckApp.l1.text = self.text


class CardWidget(ButtonBehavior, BoxLayout):
    def __init__(self, rank, suit_image):
        super(CardWidget, self).__init__(orientation='vertical',padding=10,spacing=10)

        self.rank_label = lblbtn(text=rank, font_size=50, size_hint=(None, None), size=(50, 50))
        self.suit_image = imgbtn(source=suit_image, size_hint=(None, None), size=(50, 50))
        
        self.add_widget(self.rank_label)
        self.add_widget(self.suit_image)

    def on_press(self):
        print("Pressed")
        CardDeckApp.l1 = self.rank_label


# class Deck:
#     def __init__(self):
#         self.cards = []
#         suits = ['hearts', 'diamonds', 'clubs', 'spades']
#         ranks = ['2', '3', '4', '5', '6', '7' ,'8', '9', '10','J','Q','K','A']
#         for suit in suits:
#             suit_image = f'{suit}.png'
#             for rank in ranks:
#                 card = CardWidget(rank=rank, suit_image=suit_image)
#                 self.cards.append(card) 

#     def get_cards(self):
#         return self.cards

class CardDeckApp(App):
    def build(self):
        layout = GridLayout(cols=13, padding=100, spacing=100, row_default_height=100, size_hint=(None,None), row_force_default=True)
        layout.bind(minimum_height = layout.setter('height'), minimum_width=layout.setter('width'))
        
        # deck = Deck()
        # cards = deck.get_cards()
        cardsP1 = game.players[0].hand
        cardsP1Widget = []
        for card in cardsP1:
            rank = card.rank
            suit = card.suit
            suit_image = f'{suit}.png'
            print(rank, suit_image)
            card = CardWidget(rank=rank, suit_image=suit_image)
            cardsP1Widget.append(card)

        cardsP2 = game.players[1].hand
        cardsP2Widget = []
        for card in cardsP2:
            rank = card.rank
            suit = card.suit
            suit_image = f'{suit}.png'
            print(rank, suit_image)
            card = CardWidget(rank=rank, suit_image=suit_image)
            cardsP2Widget.append(card)

        cardsP3 = game.players[2].hand
        cardsP3Widget = []
        for card in cardsP3:
            rank = card.rank
            suit = card.suit
            suit_image = f'{suit}.png'
            print(rank, suit_image)
            card = CardWidget(rank=rank, suit_image=suit_image)
            cardsP3Widget.append(card)
        
        cardsP4 = game.players[3].hand
        cardsP4Widget = []
        for card in cardsP4:
            rank = card.rank
            suit = card.suit
            suit_image = f'{suit}.png'
            print(rank, suit_image)
            card = CardWidget(rank=rank, suit_image=suit_image)
            cardsP4Widget.append(card)

        for card in cardsP1Widget:
            layout.add_widget(card)
        for card in cardsP2Widget:
            layout.add_widget(card)
        for card in cardsP3Widget:
            layout.add_widget(card)
        for card in cardsP4Widget:
            layout.add_widget(card)

        scroll_view = ScrollView(size_hint=(None, None), size=(1000, 800))
        scroll_view.add_widget(layout)

        root = BoxLayout(orientation='horizontal')
        root.add_widget(scroll_view)

        CardDeckApp.l1 = Label(text='Test', font_size=32)
       
        root.add_widget(CardDeckApp.l1)
        
        
        disp = GridLayout(cols = 1)
        disp.add_widget(root)

        return disp

if __name__ == "__main__":
    p1 = "A"
    p2 = "B"
    p3 = "C"
    p4 = "D"
    players = [p1,p2,p3,p4]
    
    game=BigTwoGame(players)
   
    CardDeckApp().run()