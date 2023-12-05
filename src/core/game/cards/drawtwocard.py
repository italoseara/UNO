from typing import Any
from .card import Card, CardColor


class DrawTwoCard(Card):
    def __init__(self, color: str):
        if color not in [CardColor.RED, CardColor.BLUE, CardColor.GREEN, CardColor.YELLOW]:
            raise ValueError(f"Invalid color: {color}")

        super().__init__(color, "draw2")

    def play(self, match: Any, player_id: int):
        match.stack += 2

        next_player = match.get_player(match.next_turn())

        if not next_player.has_draw_card():
            # Compra 4 cartas
            for _ in range(match.stack):
                next_player.add_card(match.deck.pop())

            # Passa a vez
            match.turn = match.next_turn()

            # Tira o stack
            match.stack = 0
