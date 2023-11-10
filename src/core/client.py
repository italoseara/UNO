import pygame

from core.connection import Network
from core.states import State, Menu
from engine import Engine, on_event


class Client(Engine):
    _width: int
    _height: int
    _fps: int

    _surface: pygame.Surface
    _clock: pygame.time.Clock

    __state: State
    __last_state: State

    __network: Network | None

    def __init__(self):
        super().__init__(caption="UNO in Python")
        self.__state = Menu(self)
        self.__network = None

    @property
    def state(self) -> State:
        return self.__state

    @state.setter
    def state(self, s: State) -> None:
        self.clear_components()
        self.__last_state = self.__state
        self.__state = s
        self.__state.init()

    @on_event(pygame.QUIT)
    def on_quit(self, _) -> None:
        if self.__network is not None:
            self.__network.disconnect()

    def pop_state(self, *args, **kwargs) -> None:
        self.state = self.__last_state

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
        self.__state.update_server()

    def draw(self) -> None:
        self.__state.draw(self._surface)

