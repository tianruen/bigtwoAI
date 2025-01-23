from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import BooleanProperty
from kivy.graphics import Color, Line, Rectangle

import copy
import requests

# TODO: Add undo function
# TODO: Add run MCTS function; display the action on the Kivy app

# API endpoint
url = "http://127.0.0.1:8000/agent/get_action/"

# Card suits and ranks
suits = ['Diamonds', 'Clubs', 'Hearts', 'Spades']
ranks = ['3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A', '2']
class imgbtn(ButtonBehavior, Image):
    def __init__(self, ui_ref, **kwargs):
        super(imgbtn, self).__init__(**kwargs)
        self.ui_ref = ui_ref
        
    def on_press(self):
        error = False
        if self.source == 'images/hand.png':
            for card in self.ui_ref.selected_card:
                self.ui_ref.hand_card.append([card.suit_image.source.split("/")[1].split(".")[0].capitalize(), card.rank_label.text])
            print(self.ui_ref.hand_card)
        elif self.source == 'images/next.png':
            if len(self.ui_ref.selected_card) > 1:
                for card in self.ui_ref.selected_card:
                    if card.suit_image.source == 'images/pass.png':
                        print("Error: Cannot play pass card with other cards")
                        error = True
            if not error:
                if len(self.ui_ref.selected_card) == 1 and self.ui_ref.selected_card[0].suit_image.source == 'images/pass.png':
                    hist = None
                else:
                    # hist = [[c.suit_image.source.split(".")[0].capitalize(), c.rank_label.text] for c in self.ui_ref.selected_card]
                    hist = []
                    for card in self.ui_ref.selected_card:
                        c = [card.suit_image.source.split("/")[1].split(".")[0].capitalize(), card.rank_label.text]
                        # card.suit_image.source is in the format 'images/suit.png'
                        hist.append(c)
                        if c in self.ui_ref.hand_card: self.ui_ref.hand_card.remove(c)
                        card.parent.remove_widget(card)
                    self.ui_ref.selected_card = []
                    
                self.ui_ref.history.append(hist)            
                print(self.ui_ref.history)
                
        elif self.source == 'images/run.jpg':
            opp1_played_cards = 0
            opp2_played_cards = 0
            opp3_played_cards = 0
            for i, c in enumerate(self.ui_ref.history):
                if c is not None:
                    if i % 4 == (int(self.ui_ref.idx) + 1) % 4: opp1_played_cards += len(c)
                    elif i % 4 == (int(self.ui_ref.idx)
                     + 2) % 4: opp2_played_cards += len(c)
                    elif i % 4 == (int(self.ui_ref.idx) + 3) % 4: opp3_played_cards += len(c)
                
            input_data = {
                "hand_card": self.ui_ref.hand_card,
                "hist": self.ui_ref.history,
                "opp1_num_cards": 13 - opp1_played_cards,
                "opp2_num_cards": 13 - opp2_played_cards,
                "opp3_num_cards": 13 - opp3_played_cards
            }
            
            response = requests.post(url, json=input_data)  # Send a POST request to the API
            # Check the response
            if response.status_code == 200:
                print(f"Hand Cards: {self.ui_ref.hand_card}")
                print(f"Action: {response.json()['action']}")
                
            else:
                print("Error:", response.status_code, response.text)
            
        else:
            card = self.parent
            rank = card.rank_label.text
            suit = self.source
            if suit == 'images/diamonds.png': suit = 'Diamonds'
            elif suit == 'images/clubs.png': suit = 'Clubs'
            elif suit == 'images/hearts.png': suit = 'Hearts'
            elif suit == 'images/spades.png': suit = 'Spades'
            
            card.selected = not card.selected
            if card.selected == True:
                # self.ui_ref.selected_card.append([suit, rank])
                self.ui_ref.selected_card.append(card)
                with card.canvas.before:
                    Color(0,1,0,1)
                    card.border = Line(width=2, rectangle=(card.x, card.y, 50, card.height))
            else:
                # self.ui_ref.selected_card.remove([suit, rank])
                if card in self.ui_ref.selected_card: self.ui_ref.selected_card.remove(card)
                with card.canvas.before:
                    card.canvas.before.remove(card.border)
              
class lblbtn(ButtonBehavior, Label):
    def __init__(self, ui_ref, **kwargs):
        super(lblbtn, self).__init__(**kwargs)
        self.ui_ref = ui_ref    # Store reference to the main app (CardDeckApp)
        
    def on_press(self):
        rank = self.text
        card = self.parent
        suit = card.suit_image.source
        if suit == 'images/diamonds.png': suit = 'Diamonds'
        elif suit == 'images/clubs.png': suit = 'Clubs'
        elif suit == 'images/hearts.png': suit = 'Hearts'
        elif suit == 'images/spades.png': suit = 'Spades'
 
        card.selected = not card.selected
        if card.selected == True:
            # self.ui_ref.selected_card.append([suit, rank])
            self.ui_ref.selected_card.append(card)
            with card.canvas.before:
                Color(0,1,0,1)
                card.border = Line(width=2, rectangle=(card.x, card.y, 50, card.height))
        else:
            # self.ui_ref.selected_card.remove([suit, rank])
            self.ui_ref.selected_card.remove(card)
            with card.canvas.before:
                card.canvas.before.remove(card.border)

class PlayerIndexBtn(Button):
    """
    A custom Button class to represent player index.
    """
    selected = False
    
    def __init__(self, idx, ui_ref, **kwargs):
        super().__init__(**kwargs)
        self.idx = idx
        self.text = idx
        self.background_color = (1, 1, 1, 1)  # White background initially
        self.ui_ref = ui_ref

    def on_press(self):
        """
        Toggle selection state on press.
        """
        self.selected = not self.selected
        if self.selected:
            self.ui_ref.idx = self.idx
            self.background_color = (0.5, 0.8, 1, 1)  # Light blue when selected
            for i in range(4):
                if self.idx != str(i):
                    getattr(self.ui_ref, f'idx{i}_button').background_color = (1, 1, 1, 1)
                    getattr(self.ui_ref, f'idx{i}_button').selected = False
        else:
            self.background_color = (1, 1, 1, 1)  # Reset to white
     

class CardWidget(ButtonBehavior, BoxLayout):
    def __init__(self, rank, suit_image, ui_ref):
        super(CardWidget, self).__init__(orientation='vertical',spacing=5)

        self.rank_label = lblbtn(ui_ref=ui_ref, text=rank, font_size=50, size_hint=(None, None), size=(50, 50))
        self.suit_image = imgbtn(ui_ref=ui_ref, source=suit_image, size_hint=(None, None), size=(50, 50))
        
        self.add_widget(self.rank_label)
        self.add_widget(self.suit_image)

        self.selected = False

            
class CardDeckApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.idx = None
        self.hand_card = []
        self.history = []
        self.selected_card = []
        
    def build(self):
        """
        Build the UI: 52 blocks laid out in a grid.
        """
        layout = GridLayout(cols=1, padding=100, spacing=10, row_default_height=100, size_hint=(None,None), row_force_default=True)
        layout.bind(minimum_height = layout.setter('height'), minimum_width=layout.setter('width'))
        num_rank_in_a_row = 3
        for i in range(len(ranks)//num_rank_in_a_row + 1):
            box = BoxLayout(orientation='horizontal', spacing=60)
            layout.add_widget(box)
            for r in ranks[(i*num_rank_in_a_row):((i+1)*num_rank_in_a_row)]:  # {num_rank_in_a_row} ranks per row
                for s in suits:
                    card = CardWidget(rank=r, suit_image=f'images/{s.lower()}.png', ui_ref=self)
                    box.add_widget(card)
        # pass button same row as the cards
        pass_button = CardWidget(rank="P", suit_image="images/pass.png", ui_ref=self)
        box.add_widget(pass_button)
        # new rows for hand and next buttons
        box = BoxLayout(orientation='horizontal', spacing=100)
        layout.add_widget(box)
        hand_button = CardWidget(rank="H", suit_image="images/hand.png", ui_ref=self)
        box.add_widget(hand_button)
        next_button = CardWidget(rank="N", suit_image="images/next.png", ui_ref=self)
        box.add_widget(next_button)
        run_button = CardWidget(rank="R", suit_image="images/run.jpg", ui_ref=self)
        box.add_widget(run_button)
        
        idx_container = BoxLayout(orientation='vertical', spacing=0)
        box.add_widget(idx_container)
        label_text = Label(text="Index", size_hint=(None, None), size=(200, 50), font_size=50)
        # Player index buttons
        self.idx0_button = PlayerIndexBtn("0", ui_ref=self, size_hint=(None, None), size=(50, 50))
        self.idx1_button = PlayerIndexBtn("1", ui_ref=self, size_hint=(None, None), size=(50, 50))
        self.idx2_button = PlayerIndexBtn("2", ui_ref=self, size_hint=(None, None), size=(50, 50))
        self.idx3_button = PlayerIndexBtn("3", ui_ref=self, size_hint=(None, None), size=(50, 50))
        
        idx_box = BoxLayout(orientation='horizontal', spacing=0)
        idx_box.add_widget(self.idx0_button)
        idx_box.add_widget(self.idx1_button)
        idx_box.add_widget(self.idx2_button)
        idx_box.add_widget(self.idx3_button)
        # Add text and buttons to the layout
        idx_container.add_widget(label_text)
        idx_container.add_widget(idx_box)
        
        scroll_view = ScrollView(size_hint=(None, None), size=(1000, 800))
        scroll_view.add_widget(layout)

        root = BoxLayout(orientation='horizontal')
        root.add_widget(scroll_view)
        return root

if __name__ == '__main__':
    CardDeckApp().run()
