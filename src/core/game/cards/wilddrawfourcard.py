from .card import Card, CardColor


class WildDrawFourCard(Card):
    def __init__(self):
        super().__init__("wild", "draw4")

    def play(self, game):
        pass
