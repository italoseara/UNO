import pygame

from core.connection import Network
from core.graphics import Gfx
from .state import State
from .join import Join

from assets.components import Button, Text, TextInput


class Menu(State):

    def init(self):
        self.client.add_component(
            Button("Join", 50, 300,
                   font_size=72,
                   text_align="left",
                   on_click=self.change_state))

        self.client.add_component(
            Button("Host", 50, 350,
                   font_size=72,
                   text_align="left",
                   on_click=self.change_state))

        self.client.add_component(
            Button("Credits", 50, 400,
                   font_size=72,
                   text_align="left",
                   on_click=self.change_state))

        self.client.add_component(
            Text("UESC (2023)", 10, 580, font_size=16))

    def change_state(self, button: Button):
        state = self.client.state
        match button.text:
            case "Join":
                state = Join(self.client)
            case name:
                print(name)

        self.client.state = state

    def update(self, dt: float):
        pass

    def update_server(self, network: Network):
        pass

    def draw(self, surface: pygame.Surface):
        # Desenha o fundo
        surface.blit(Gfx.BACKGROUND, (0, 0))
