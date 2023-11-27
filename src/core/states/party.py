import pygame

from assets.components import Text, Button
from core.game.match import Match
from core.game.player import Player
from core.graphics import Resources
from core.connection import Network

from .menu import Menu
from .state import State


class Party(State):
    __match: Match | None
    __id: int

    # Imagens salvas para não ter que ficar redimensionando toda hora
    __flipped_left: pygame.Surface
    __flipped_right: pygame.Surface
    __flipped_front: pygame.Surface

    def __init__(self, client):
        super().__init__(client)
        self.__match = None
        self.__id = -1

        card_width = int(Resources.CARD_BACK.get_width() * 3.5)
        card_height = int(Resources.CARD_BACK.get_height() * 3.5)
        size = (card_width, card_height)

        self.__flipped_left = pygame.transform.scale(Resources.CARD_BACK, size)
        self.__flipped_left = pygame.transform.rotate(self.__flipped_left, 90).convert()

        self.__flipped_right = pygame.transform.scale(Resources.CARD_BACK, size)
        self.__flipped_right = pygame.transform.rotate(self.__flipped_left, -90).convert()

        self.__flipped_front = pygame.transform.scale(Resources.CARD_BACK, size).convert()

    def init(self):
        cx = self._client.width // 2
        cy = self._client.height // 2

        self._client.add_component(
            Text("Party", cx, cy, font_color="black", font_size=72, align="center"))

        self._client.add_component(
            Button("< Back", 10, 560, height=30, font_size=32, on_click=self.__exit_party))

    def __exit_party(self, *_):
        self._client.disconnect()
        self._client.close_server()
        self._client.state = Menu(self._client)

    def update(self, dt: float):
        pass

    def update_server(self, network: Network):
        if network is None:
            return

        # Se a partida já começou, volta para o menu de join
        self.__id = network.id
        if self.__id == -1:
            self.__exit_party()
            return

        self.__match = network.send({"type": "GET"})

    def __draw_own_hand(self, surface: pygame.Surface, player: Player):
        cx = self._client.width // 2

        card_width = player.hand[0].image.get_width()  # Largura de uma carta
        max_width = 600  # Largura máxima que a mão pode ter em píxeis
        max_space = -30  # Espaço máximo entre as cartas

        space = min(card_width + max_space, max_width // len(player.hand))  # Espaço entre as cartas
        hand_width = (len(player.hand) - 1) * space + card_width  # Largura da mão em píxeis

        for i, card in enumerate(player.hand):
            surface.blit(card.image, (
                cx - hand_width // 2 + i * space,
                self._client.height - 20 - card.image.get_height()))

    def __draw_other_hand(self, surface: pygame.Surface):
        players_len = self.__match.get_number_of_players()

        # Pega os IDs dos jogadores ao redor do jogador atual
        left_id = None
        right_id = None
        front_id = None

        if players_len == 4:
            left_id = (self.__id + 1) % players_len
            right_id = (self.__id - 1) % players_len
            front_id = (self.__id + 2) % players_len
        elif players_len == 3:
            left_id = (self.__id + 1) % players_len
            right_id = (self.__id - 1) % players_len
        elif players_len == 2:
            front_id = (self.__id + 1) % players_len

        if left_id is not None:
            player = self.__match.get_player(left_id)
            if player is not None and player.hand:
                self.__draw_left_hand(surface, player)

        if right_id is not None:
            player = self.__match.get_player(right_id)
            if player is not None and player.hand:
                self.__draw_right_hand(surface, player)

        if front_id is not None:
            player = self.__match.get_player(front_id)
            if player is not None and player.hand:
                self.__draw_front_hand(surface, player)

    def __draw_left_hand(self, surface: pygame.Surface, player: Player):
        cy = self._client.height // 2

        card_height = self.__flipped_left.get_height()  # Altura de uma carta
        max_height = 400  # Altura máxima que a mão pode ter em píxeis
        max_space = -30  # Espaço máximo entre as cartas

        space = min(card_height + max_space, max_height // len(player.hand))  # Espaço entre as cartas
        hand_height = (len(player.hand) - 1) * space + card_height  # Altura da mão em píxeis

        for i, card in enumerate(player.hand):
            surface.blit(self.__flipped_left, (20, cy - hand_height // 2 + i * space))

    def __draw_right_hand(self, surface: pygame.Surface, player: Player):
        cy = self._client.height // 2

        card_height = self.__flipped_right.get_height()
        card_width = self.__flipped_right.get_width()
        max_height = 400
        max_space = -30

        space = min(card_height + max_space, max_height // len(player.hand))
        hand_height = (len(player.hand) - 1) * space + card_height

        for i, card in enumerate(player.hand):
            surface.blit(self.__flipped_right, (self._client.width - 20 - card_width, cy - hand_height // 2 + i * space))

    def __draw_front_hand(self, surface: pygame.Surface, player: Player):
        cx = self._client.width // 2

        card_width = self.__flipped_front.get_width()
        max_width = 600
        max_space = -30

        space = min(card_width + max_space, max_width // len(player.hand))
        hand_width = (len(player.hand) - 1) * space + card_width

        for i, card in enumerate(player.hand):
            surface.blit(self.__flipped_front, (cx - hand_width // 2 + i * space, 20))

    def draw(self, surface: pygame.Surface):
        surface.blit(Resources.BACKGROUND, (0, 0))

        if self.__match is None or not self.__match.ready:
            return

        player = self.__match.get_player(self.__id)
        if player.hand:
            self.__draw_own_hand(surface, player)
        self.__draw_other_hand(surface)
