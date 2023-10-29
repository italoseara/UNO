import pygame

from core.match import Match
from core.connection import Network
from engine import Engine, on_event

from assets.components import Component, Button


class Client(Engine):
    width: int
    height: int
    fps: int

    surface: pygame.Surface
    clock: pygame.time.Clock

    match: Match | None
    network: Network

    components: list[Component]

    def __init__(self):
        super().__init__(caption="PyNO")
        self.network = Network("192.168.0.248", 5555)
        self.match = None
        self.components = []

    @on_event(pygame.QUIT)
    def on_quit(self, _) -> None:
        self.network.disconnect()

    def init(self) -> None:
        self.components.append(
            Button(50, 50, 100, 50, "Play",
                   background_color="green", border_width=5, action=lambda: print("Play")))

    def update(self, dt: float) -> None:
        self.match = self.network.send("get")
        for comp in self.components:
            comp.update(dt)

    def draw(self) -> None:
        self.surface.fill((255, 255, 255))
        for comp in self.components:
            comp.draw(self.surface)

