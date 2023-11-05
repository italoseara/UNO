import pygame

from core.connection import Network
from core.graphics import Gfx
from .state import State
from .join import Join

from assets.components import Button, TextInput


class Menu(State):

    def init(self):
        self.client.add_component("join", Button(160, 300, 250, 50, "Join",
                                                 font_size=72,
                                                 text_align="left",
                                                 on_click=self.change_state))
        self.client.add_component("host", Button(160, 350, 250, 50, "Host",
                                                 font_size=72,
                                                 text_align="left",
                                                 on_click=self.change_state))
        self.client.add_component("credits", Button(160, 400, 250, 50, "Credits",
                                                    font_size=72,
                                                    text_align="left",
                                                    on_click=self.change_state))

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
