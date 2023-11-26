from random import shuffle

from .player import Player
from .cards.card import Card


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

    def get_hand(self, player_id: id) -> list[Card]:
        """Retorna a mão de um jogador

        Args:
            player_id (int): ID do jogador

        Returns:
            list[Card]: Mão do jogador
        """

        for player in self.__players:
            if player.id == player_id:
                return player.hand

        return []

    def start(self) -> None:
        """Inicia a partida"""

        self.__ready = True
        # TODO: Criar baralho com 112 cartas
        # Cartas de 0 a 9, 2x cada para cada cor
        # Cartas especiais, 2x cada para cada cor
        # Cartas coringa, 4x cada
        self.__deck = []
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

    def remove_player(self, player_id: id) -> None:
        raise NotImplementedError("Not implemented yet")
