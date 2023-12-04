from typing import Any
from .card import Card, CardColor


class ReverseCard(Card):
    def __init__(self, color: str):
        if color not in [CardColor.RED, CardColor.BLUE, CardColor.GREEN, CardColor.YELLOW]:
            raise ValueError(f"Invalid color: {color}")

        super().__init__(color, "reverse")

    def play(self, match: Any, player_id: int):
        # Inverte o sentido do jogo
        match.turn_direction *= -1
