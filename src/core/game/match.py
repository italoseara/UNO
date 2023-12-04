import random
from util import Queue

from .player import Player
from .deck import Deck
from .cards import Card, CardColor


class CardMount:
    def __init__(self, card: Card, rotation: int = None, offset: tuple[int, int] = None) -> None:
        self.__card = card
        self.__rotation = random.randint(-80, 80) if rotation is None else rotation
        self.__offset = (random.randint(-10, 10), random.randint(-10, 10)) if offset is None else offset

    @property
    def card(self) -> Card:
        return self.__card

    @property
    def rotation(self) -> int:
        return self.__rotation

    @property
    def offset(self) -> tuple[int, int]:
        return self.__offset


class Match:
    def __init__(self) -> None:
        self.__ready = False
        self.__turn = 0

        self.__players = []

        self.__deck = Deck()
        self.__discard = Queue[CardMount]()

    @property
    def ready(self) -> bool:
        return self.__ready

    @property
    def host_online(self) -> bool:
        return 0 in [player.id for player in self.players]

    @property
    def players(self) -> list[Player]:
        return self.__players

    @property
    def deck(self) -> Deck:
        return self.__deck

    @property
    def discard(self) -> Queue[CardMount]:
        return self.__discard

    @property
    def turn(self) -> int:
        return self.__turn

    def is_full(self) -> bool:
        return len(self.__players) == 4

    def is_playable(self, card: Card) -> bool:
        top = self.__discard.peek()
        if top is None:
            return False

        # TODO: Wild cards can change color
        return top.card.color == CardColor.WILD or \
            card.color == CardColor.WILD or \
            card.color == top.card.color or \
            card.value == top.card.value

    def can_draw(self, player_id: int) -> bool:
        playable_cards = [card for card in self.get_player(player_id).hand if self.is_playable(card)]
        return len(playable_cards) == 0

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

    def get_number_of_players(self) -> int:
        """Retorna o número de jogadores na partida"""

        return len(self.__players)

    def start(self) -> None:
        """Inicia a partida"""

        self.__ready = True

        # Sorteia o jogador inicial
        self.__turn = random.randint(0, len(self.__players) - 1)

        # Coloca uma carta no monte de descarte
        self.__discard.push(CardMount(self.__deck.pop(), 0, (0, 0)))

    def add_player(self, player_id: id, player_name: str) -> None:
        """Adiciona um jogador à partida

        Args:
            player_id (int): ID do jogador
            player_name (str): Nome do jogador
        """
        player = Player(id=player_id, name=player_name)

        # Distribui 7 cartas para cada jogador
        for _ in range(7):
            player.add_card(self.__deck.pop())
        self.__players.append(player)

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

    def play(self, player_id: int, card_index: int) -> None:
        """Joga uma carta

        Args:
            player_id (int): ID do jogador
            card_index (int): Índice da carta na mão do jogador
        """

        player = self.get_player(player_id)
        card = player.remove_card(card_index)

        self.__discard.push(CardMount(card))
        # TODO: Verifica se o jogador ganhou
        card.play(self)
        self.__turn = (self.__turn + 1) % len(self.__players)

    def draw(self, player_id: int) -> None:
        """Compra uma carta

        Args:
            player_id (int): ID do jogador
        """

        player = self.get_player(player_id)
        player.add_card(self.__deck.pop())
