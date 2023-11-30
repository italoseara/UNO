from .card import Card, CardColor


class DrawTwoCard(Card):
    def __init__(self, color: str):
        if color not in [CardColor.RED, CardColor.BLUE, CardColor.GREEN, CardColor.YELLOW]:
            raise ValueError(f"Invalid color: {color}")

        super().__init__(color, "draw2")

    def play(self, game):
        pass
