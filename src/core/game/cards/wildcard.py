from typing import Any
from .card import Card, CardColor


class WildCard(Card):
    def __init__(self):
        super().__init__(CardColor.WILD, "select_color")

    def play(self, match: Any, player_id: int):
        player = match.get_player(player_id)
        player.selecting_color = True
