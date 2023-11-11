import pygame

from core.graphics import Gfx
from assets.components import Button, Text

from .state import State


class Menu(State):

    def init(self):
        self._client.add_component(
            Button("Join", 50, 300,
                   font_size=72,
                   on_click=self.change_state))

        self._client.add_component(
            Button("Host", 50, 350,
                   font_size=72,
                   on_click=self.change_state))

        self._client.add_component(
            Button("Credits", 50, 400,
                   font_size=72,
                   on_click=self.change_state))

        self._client.add_component(
            Text("UESC (2023)", 10, 580, font_size=16))

    def change_state(self, button: Button):
        match button.text:
            case "Join":
                from .join import Join
                state = Join(self._client)
            case "Credits":
                from .credits import Credits
                state = Credits(self._client)
            case _:
                return

        self._client.state = state

    def update(self, dt: float):
        pass

    def update_server(self):
        pass

    def draw(self, surface: pygame.Surface):
        # Desenha o fundo
        surface.blit(Gfx.MENU_BACKGROUND, (0, 0))
