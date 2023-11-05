import pygame

from assets.states import State, Menu
from engine import Engine, on_event

from core.connection import Network


class Client(Engine):
    width: int
    height: int
    fps: int

    surface: pygame.Surface
    clock: pygame.time.Clock

    state: State

    network: Network | None

    def __init__(self):
        super().__init__(caption="UNO in Python")
        self.state = Menu(self)
        self.network = None

    @on_event(pygame.QUIT)
    def on_quit(self, _) -> None:
        if self.network is not None:
            self.network.disconnect()

    def connect(self, ip: str, port: int) -> None:
        if self.network is not None:
            self.network.disconnect()

        self.network = Network(ip, port)

    def disconnect(self) -> None:
        if self.network is not None:
            self.network.disconnect()
            self.network = None

    def set_state(self, state) -> None:
        self.clear_components()
        self.state = state(self)
        self.state.init()

    def init(self) -> None:
        self.state.init()

    def update(self, dt: float) -> None:
        self.state.update(dt)

    def update_server(self) -> None:
        self.state.update_server(self.network)

    def draw(self) -> None:
        self.state.draw(self.surface)

