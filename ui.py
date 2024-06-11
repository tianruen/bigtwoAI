from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.scrollview import ScrollView

class CardWidget(BoxLayout):
    def __init__(self, rank, suit_image):
        super(CardWidget, self).__init__(orientation='vertical',padding=10,spacing=10)

        self.rank_label = Label(text=rank, font_size=50, size_hint=(None, None), size=(50, 50))
        self.suit_image = Image(source=suit_image, size_hint=(None, None), size=(50, 50))
        
        self.add_widget(self.rank_label)
        self.add_widget(self.suit_image)

class Deck:
    def __init__(self):
        self.cards = []
        suits = ['hearts', 'diamonds', 'clubs', 'spades']
        ranks = ['2', '3', '4', '5', '6', '7' ,'8', '9', '10','J','Q','K','A']
        for suit in suits:
            suit_image = f'{suit}.png'
            for rank in ranks:
                card = CardWidget(rank=rank, suit_image=suit_image)
                self.cards.append(card)

    def get_cards(self):
        return self.cards

class CardDeckApp(App):
    def build(self):
        layout = GridLayout(cols=13, padding=100, spacing=100, row_default_height=100, size_hint=(None,None), row_force_default=True)
        layout.bind(minimum_height = layout.setter('height'), minimum_width=layout.setter('width'))
        
        deck = Deck()
        cards = deck.get_cards()

        for card in cards:
            layout.add_widget(card)

        scroll_view = ScrollView(size_hint=(None, None), size=(800, 600))
        scroll_view.add_widget(layout)

        root = BoxLayout(orientation='horizontal')
        root.add_widget(scroll_view)
        return root


if __name__ == "__main__":
    CardDeckApp().run()