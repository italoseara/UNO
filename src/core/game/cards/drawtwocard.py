from typing import Any
from .card import Card, CardColor


class DrawTwoCard(Card):
    def __init__(self, color: str):
        if color not in [CardColor.RED, CardColor.BLUE, CardColor.GREEN, CardColor.YELLOW]:
            raise ValueError(f"Invalid color: {color}")

        super().__init__(color, "draw2")

    def play(self, match: Any, player_id: int):
        # TODO: Stackar os +4 e +2

        next_player = match.next_turn()
        for _ in range(2):
            match.draw(next_player)

        match.turn = match.next_turn()
