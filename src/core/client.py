import pygame

from engine import Engine, on_event

from core.graphics.gfx import Gfx
from core.match import Match
from core.connection import Network

from assets.components import Button, TextInput


class Client(Engine):
    width: int
    height: int
    fps: int

    surface: pygame.Surface
    clock: pygame.time.Clock

    match: Match | None
    network: Network

    def __init__(self):
        super().__init__(caption="UNO in Python")
        self.network = Network("localhost", 5555)
        self.match = None

    @on_event(pygame.QUIT)
    def on_quit(self, _) -> None:
        self.network.disconnect()

    def init(self) -> None:
        self.clear_components()
        self.add_component("join", Button(100, 300, 160, 50, "Join",
                                          font_size=72,
                                          text_align="left",
                                          on_click=lambda b: print(b.text)))
        self.add_component("host", Button(100, 350, 160, 50, "Host",
                                          font_size=72,
                                          text_align="left",
                                          on_click=lambda b: print(b.text)))
        self.add_component("credits", Button(100, 400, 160, 50, "Credits",
                                             font_size=72,
                                             text_align="left",
                                             on_click=lambda b: print(b.text)))

    def update(self, dt: float) -> None:
        self.match = self.network.send("get")

    def draw(self) -> None:
        # Desenha o fundo
        self.surface.blit(Gfx.BACKGROUND, (0, 0))

        # Deixa tela escura
        transparent = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        transparent.fill((0, 0, 0, 50))
        self.surface.blit(transparent, (0, 0))

        # Desenha o logo
        self.surface.blit(Gfx.LOGO, (50, 50))
