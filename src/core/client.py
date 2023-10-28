import pygame

from core.match import Match
from core.connection import Network
from engine import Engine, on_event


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
        self.network = Network("192.168.0.248", 5555)
        self.match = None

    @on_event(pygame.QUIT)
    def on_quit(self, _) -> None:
        self.network.disconnect()

    def init(self) -> None:
        pass

    def update(self, dt: float) -> None:
        self.match = self.network.send("get")

    def draw(self) -> None:
        self.surface.fill((255, 255, 255))
