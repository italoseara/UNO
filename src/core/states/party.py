import pygame

from assets.components import Text, Button, TextInput
from core.graphics import Gfx
from .state import State


class Party(State):
    def init(self):
        cx = self._client.width // 2
        cy = self._client.height // 2

        self._client.add_component(
            Text("Party", cx, cy,font_color="black", font_size=72, align="center"))

    def update(self, dt: float):
        pass

    def update_server(self):
        pass

    def draw(self, surface: pygame.Surface):
        surface.blit(Gfx.CREDITS_BACKGROUND, (0, 0))
