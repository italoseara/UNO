from random import shuffle

from .cards import *
from .player import Player


class Match:
    __ready: bool
    __players: list[Player]
    __deck: list[Card]

    def __init__(self):
        self.__ready = False
        self.__players = []
        self.__deck = []

    @property
    def ready(self) -> bool:
        return self.__ready

    @property
    def players(self) -> list[Player]:
        return self.__players

    @property
    def deck(self) -> list[Card]:
        return self.__deck

    def get_hand(self, player_id: id) -> list[Card] | None:
        """Retorna a mão de um jogador

        Args:
            player_id (int): ID do jogador

        Returns:
            list[Card]: Mão do jogador
        """

        for player in self.__players:
            if player.id == player_id:
                return player.hand
        return None

    def start(self) -> None:
        """Inicia a partida"""

        self.__ready = True
        self.__deck = []
        for color in [CardColor.RED, CardColor.GREEN, CardColor.BLUE, CardColor.YELLOW]:
            for number in range(10):
                for _ in range(2):
                    self.__deck.append(NumberCard(color=color, value=str(number)))

            for _ in range(2):
                self.__deck.append(DrawTwoCard(color=color))
                self.__deck.append(SkipCard(color=color))
                self.__deck.append(ReverseCard(color=color))

        for _ in range(4):
            self.__deck.append(WildCard())
            self.__deck.append(WildDrawFourCard())

        shuffle(self.__deck)

        # TODO: Distribuir cartas

    def add_player(self, player_id: id, player_name: str) -> None:
        """Adiciona um jogador à partida

        Args:
            player_id (int): ID do jogador
            player_name (str): Nome do jogador
        """

        self.__players.append(Player(id=player_id, name=player_name))

        if len(self.__players) == 2:
            self.start()

    def remove_player(self, player_id: id) -> str | None:
        """Remove um jogador da partida

        Args:
            player_id (int): ID do jogador

        Returns:
            str | None: Nome do jogador
        """

        for player in self.__players:
            if player.id == player_id:
                self.__players.remove(player)
                return player.name
        return None
