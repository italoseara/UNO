import pygame

from assets.components import Text, Button, TextInput
from core.graphics import Gfx
from . import Menu
from .state import State


class Party(State):
    def init(self):
        cx = self._client.width // 2
        cy = self._client.height // 2

        self._client.add_component(
            Text("Party", cx, cy, font_color="black", font_size=72, align="center"))

        self._client.add_component(
            Button("< Back", 10, 560, height=30, font_size=32, on_click=self.__exit_party))

    def __exit_party(self, button: Button):
        self._client.state = Menu(self._client)

    def update(self, dt: float):
        pass

    def update_server(self):
        pass

    def draw(self, surface: pygame.Surface):
        surface.blit(Gfx.BACKGROUND, (0, 0))
