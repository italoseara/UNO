import random
from util import Queue

from .player import Player
from .deck import Deck
from .cards import Card, CardColor, WildCard


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
        self.__over = False

        self.__turn = 0
        self.__turn_direction = 1

        self.__stack = 0

        self.__players = []

        self.__deck = Deck()
        self.__discard = Queue[CardMount]()
        self.__already_played = Queue[Card]()

    @property
    def ready(self) -> bool:
        return self.__ready

    @property
    def over(self) -> bool:
        return self.__over

    @property
    def turn(self) -> int:
        return self.__turn

    @turn.setter
    def turn(self, value: int) -> None:
        self.__turn = value

    @property
    def turn_direction(self) -> int:
        return self.__turn_direction

    @turn_direction.setter
    def turn_direction(self, value: int) -> None:
        self.__turn_direction = value

    @property
    def stack(self) -> int:
        return self.__stack

    @stack.setter
    def stack(self, value: int) -> None:
        self.__stack = value

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

    def is_full(self) -> bool:
        return len(self.__players) == 4

    def is_playable(self, card: Card) -> bool:
        top = self.__discard.peek()
        if top is None:
            return False

        if self.__stack > 0:
            return card.value in ["draw2", "draw4"]

        return top.card.color == CardColor.WILD or \
            card.color == CardColor.WILD or \
            card.color == top.card.color or \
            card.value == top.card.value

    def can_draw(self, player_id: int) -> bool:
        if self.__over:
            return False

        playable_cards = [card for card in self.get_player(player_id).hand if self.is_playable(card)]
        return len(playable_cards) == 0

    def can_play(self, player_id: int) -> bool:
        if self.__over:
            return False

        player = self.get_player(player_id)
        return self.__turn == player_id and not player.selecting_color

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

    def next_turn(self) -> int:
        return (self.__turn + self.__turn_direction) % len(self.__players)

    def start(self) -> None:
        """Inicia a partida"""

        self.__ready = True
        self.__over = False

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
        if len(self.__discard) > 5:
            # Coloca as cartas de baixo do monte de descarte no monte de já jogadas,
            # para evitar que o jogo fique muito pesado
            self.__already_played.push(self.__discard.pop().card)

        # Caso o monte de cartas esteja vazio ou o monte de já jogadas esteja muito grande,
        if len(self.__already_played) > 10 or len(self.__deck) == 0:
            # Coloca as cartas já jogadas de volta no monte de cartas e embaralha
            for i in range(len(self.__already_played)):
                card = self.__already_played.pop()
                if isinstance(card, WildCard):
                    card.color = CardColor.WILD
                self.__deck.push(card)
            self.__deck.shuffle()

        if len(player.hand) == 0:
            # Fim de jogo
            self.__over = True
            return

        card.play(self, player_id)

        # Passa a vez
        if not player.selecting_color:
            self.__turn = self.next_turn()

    def draw(self, player_id: int) -> None:
        """Compra uma carta

        Args:
            player_id (int): ID do jogador
        """

        player = self.get_player(player_id)
        player.add_card(self.__deck.pop())

    def select_color(self, player_id: int, color: str):
        """Seleciona uma cor

        Args:
            player_id (int): ID do jogador
            color (str): Cor selecionada
        """

        card = self.__discard.peek().card
        if not isinstance(card, WildCard):
            raise TypeError(f"Card {card} is not a WildCard")

        card.color = color
        card.after_play(self, player_id)
