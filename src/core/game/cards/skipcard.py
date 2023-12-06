from typing import Any
from .card import Card, CardColor


class SkipCard(Card):
    def __init__(self, color: str):
        if color not in [CardColor.RED, CardColor.BLUE, CardColor.GREEN, CardColor.YELLOW]:
            raise ValueError(f"Invalid color: {color}")

        super().__init__(color, "skip")

    def play(self, match: Any, player_id: int):
        # Pula o próximo jogador
        match.next_turn()
