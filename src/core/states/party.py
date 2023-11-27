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

    def __init__(self, client):
        super().__init__(client)
        self.__match = None
        self.__id = -1

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

    def __draw_hand(self, surface: pygame.Surface, player: Player):
        cx = self._client.width // 2

        card_width = player.hand[0].image.get_width()  # Largura de uma carta
        max_width = 600  # Largura máxima que a mão pode ter em píxeis
        max_space = 2  # Espaço máximo entre as cartas

        space = min(card_width + max_space, max_width // len(player.hand))  # Espaço entre as cartas
        hand_width = len(player.hand) * space  # Largura da mão em píxeis

        for i, card in enumerate(player.hand):
            surface.blit(card.image, (cx - hand_width // 2 + i * space, 400))

    def draw(self, surface: pygame.Surface):
        surface.blit(Resources.BACKGROUND, (0, 0))

        if self.__match is None or not self.__match.ready:
            return

        player = self.__match.get_player(self.__id)
        if player is None:
            return

        if player.hand:
            self.__draw_hand(surface, player)
