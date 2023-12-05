from typing import Any
from .card import CardColor, Card
from .wildcard import WildCard


class WildDrawFourCard(WildCard):
    def __init__(self):
        Card.__init__(self, CardColor.WILD, "draw4")

    def play(self, match: Any, player_id: int):
        # Seleciona a cor da carta
        super().play(match, player_id)

    def after_play(self, match: Any, player_id: int):
        match.stack += 4

        next_player = match.get_player(match.next_turn())

        if not next_player.has_draw_card():
            # Compra 4 cartas
            for _ in range(match.stack):
                next_player.add_card(match.deck.pop())

            # Passa a vez
            match.turn = match.next_turn()

            # Tira o stack
            match.stack = 0

        super().after_play(match, player_id)
