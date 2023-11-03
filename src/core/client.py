import pygame
import socket

from core.match import Match
from core.connection import Network
from engine import Engine, on_event

from assets.components import Button, Text_input


class Client(Engine):
    width: int
    height: int
    fps: int

    surface: pygame.Surface
    clock: pygame.time.Clock

    match: Match | None
    network: Network

    def __init__(self):
        super().__init__(caption="PyNO")
        self.network = Network("localhost", 5555)
        self.match = None

    @on_event(pygame.QUIT)
    def on_quit(self, _) -> None:
        self.network.disconnect()

    def init(self) -> None:
        self.clear_components()
        self.add_component(Button(50, 50, 100, 50, "Play",
                                  background_color="green",
                                  border_width=5,
                                  border_radius=10,
                                  on_click=lambda b: print("Play")))
        self.add_component(Text_input(200, 200, 100, 50,
                                      text_size=20,
                                      border_radius=5,
                                      background_color=None,
                                      border_width=5))

    def update(self, dt: float) -> None:
        self.match = self.network.send("get")

    def draw(self) -> None:
        self.surface.fill((255, 255, 0))
