from .card import Card, CardColor


class NumberCard(Card):
    def __init__(self, color: str, value: str):
        if color not in [CardColor.RED, CardColor.BLUE, CardColor.GREEN, CardColor.YELLOW]:
            raise ValueError(f"Invalid color: {color}")

        if value not in [str(i) for i in range(10)]:
            raise ValueError(f"Invalid value: {value}")

        super().__init__(color, value)

    def play(self, game):
        pass
