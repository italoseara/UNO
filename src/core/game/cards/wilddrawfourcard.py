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
        next_player = match.next_turn()

        # TODO: Stackar os +4 e +2

        # Pega 4 cartas
        for _ in range(4):
            match.draw(next_player)

        # Pula o próximo jogador
        match.turn = match.next_turn()

        super().after_play(match, player_id)
