from typing import Any
from .card import CardColor, Card
from .wildcard import WildCard


class WildDrawFourCard(WildCard):
    def __init__(self):
        Card.__init__(self, CardColor.WILD, "select_color")

    def play(self, match: Any, player_id: int):
        super().play(match, player_id)
