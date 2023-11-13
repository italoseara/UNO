import pygame

from assets.components import Text, Button
from core.graphics import Gfx

from .state import State


class Credits(State):
    __random_cards: list[pygame.Surface]

    def init(self):
        self.__random_cards = []
        self.__random_cards.append(pygame.transform.rotate(Gfx.random_card(), 15))
        self.__random_cards.append(pygame.transform.rotate(Gfx.random_card(), -15))

        cx = self._client.width // 2
        cy = self._client.height // 2

        self._client.add_component(
            Text("Credits", cx, 60, font_size=72, align="center"))

        self._client.add_component(
            Text("Professor", cx, 170, font_size=50, align="center"))
        self._client.add_component(
            Text("Dany Sanchez Dominguez", cx, 210, font_size=30, align="center"))

        self._client.add_component(
            Text("Students", cx, 290, font_size=50, align="center"))
        self._client.add_component(
            Text("Italo Seara + Lucas Luige", cx, 330, font_size=30, align="center"))

        self._client.add_component(
            Text("University", cx, 410, font_size=50, align="center"))
        self._client.add_component(
            Text("Universidade Estadual de Santa Cruz (UESC)", cx, 450, font_size=30, align="center"))

        self._client.add_component(
            Button("< Back", 10, 560, height=30, font_size=32, on_click=self._client.pop_state))

    def update(self, dt: float):
        pass

    def update_server(self):
        pass

    def draw(self, surface: pygame.Surface):
        surface.blit(Gfx.BACKGROUND, (0, 0))
        surface.blit(self.__random_cards[0], (40, 130))
        surface.blit(self.__random_cards[1], (610, 210))
