from .player import Player
from .deck import Deck
from .cards import Card


class Match:
    __ready: bool
    __stopped: bool
    __deck: Deck | None
    __players: list[Player]

    def __init__(self):
        self.__ready = False
        self.__stopped = False
        self.__players = []
        self.__deck = Deck()

    @property
    def ready(self) -> bool:
        return self.__ready

    @property
    def stopped(self) -> bool:
        return self.__stopped

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

    def stop(self):
        """Para a partida"""

        self.__stopped = True

    def add_player(self, player_id: id, player_name: str) -> None:
        """Adiciona um jogador à partida

        Args:
            player_id (int): ID do jogador
            player_name (str): Nome do jogador
        """
        player = Player(id=player_id, name=player_name)

        # Distribui 7 cartas para cada jogador
        for _ in range(7):
            player.add_card(self.__deck.draw_card())
        self.__players.append(player)

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
                for card in player.hand:
                    self.__deck.push(card)
                self.__players.remove(player)
                return player.name
        return None
