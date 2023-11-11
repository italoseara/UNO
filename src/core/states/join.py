import pygame

from .state import State
from core.graphics import Gfx
from assets.components import Button, Text, TextInput

class Join(State):
    def init(self):
        cx = self._client.width // 2
        cy = self._client.height // 2

        self._client.add_component(
            Button("Back", 10, 560, height=30, font_size=32, on_click=self._client.pop_state))

        self._client.add_component(
            Text("Insert the port", cx, 200, font_size=50, align="center"))

        self._client.add_component(
            TextInput(cy, 250, 200, 50, font_size=30, max_length_input= 5,
                      text_align="center", font_color="black", background_color="white",
                      border_radius=15, border_width=5, border_color="gray", catch=True)
        )

        self._client.add_component(
            Button("Click here to join server", 3*cx//6,cy, height=50, font_size=35,
                   on_click=self._client.pop_state)) # TODO: Implementar ação do botão


    def update(self, dt: float):
        pass

    def update_server(self):
        pass

    def draw(self, surface: pygame.Surface):
        surface.blit(Gfx.CREDITS_BACKGROUND, (0, 0))
