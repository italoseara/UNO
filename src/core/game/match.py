from .player import Player
from .deck import Deck
from .cards import Card


class Match:
    __ready: bool
    __players: list[Player]
    __deck: Deck | None

    def __init__(self):
        self.__ready = False
        self.__deck = None
        self.__players = []

    @property
    def ready(self) -> bool:
        return self.__ready

    @property
    def players(self) -> list[Player]:
        return self.__players

    @property
    def deck(self) -> Deck:
        return self.__deck

    def get_player(self, player_id: id) -> Player | None:
        """Retorna a mão de um jogador

        Args:
            player_id (int): ID do jogador

        Returns:
            list[Card]: Mão do jogador
        """

        for player in self.__players:
            if player.id == player_id:
                return player
        return None

    def get_number_of_players(self) -> int:
        """Retorna o número de jogadores na partida"""

        return len(self.__players)

    def start(self) -> None:
        """Inicia a partida"""

        self.__ready = True
        self.__deck = Deck()

        # Distribuir 7 cartas para cada jogador
        for player in self.__players:
            for _ in range(7):
                player.add_card(self.__deck.draw_card())

    def add_player(self, player_id: id, player_name: str) -> None:
        """Adiciona um jogador à partida

        Args:
            player_id (int): ID do jogador
            player_name (str): Nome do jogador
        """

        self.__players.append(Player(id=player_id, name=player_name))

        if len(self.__players) == 4:
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
