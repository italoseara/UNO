from .card import Card, CardColor


class WildCard(Card):
    def __init__(self):
        super().__init__("wild", "select_color")

    def play(self, game):
        pass
