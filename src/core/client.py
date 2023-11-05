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

    __state: State

    __network: Network | None

    def __init__(self):
        super().__init__(caption="UNO in Python")
        self.__state = Menu(self)
        self.__network = None

    @on_event(pygame.QUIT)
    def on_quit(self, _) -> None:
        if self.__network is not None:
            self.__network.disconnect()

    @property
    def state(self) -> State:
        return self.__state

    @state.setter
    def state(self, s) -> None:
        self.clear_components()
        self.__state = s(self)
        self.__state.init()

    def connect(self, ip: str, port: int) -> None:
        if self.__network is not None:
            self.__network.disconnect()

        self.__network = Network(ip, port)

    def disconnect(self) -> None:
        if self.__network is not None:
            self.__network.disconnect()
            self.__network = None

    def init(self) -> None:
        self.__state.init()

    def update(self, dt: float) -> None:
        self.__state.update(dt)

    def update_server(self) -> None:
        self.__state.update_server(self.__network)

    def draw(self) -> None:
        self.__state.draw(self.surface)

