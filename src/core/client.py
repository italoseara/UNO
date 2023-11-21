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
        """Evento de saída do jogo."""

        if self.__network is not None:
            self.__network.disconnect()

    def pop_state(self, *args, **kwargs) -> None:
        """Retorna ao estado anterior."""

        self.state = self.__last_state

    def connect(self, ip: str, port: int) -> None:
        """Conecta ao servidor."""

        if self.__network is not None:
            self.__network.disconnect()

        self.__network = Network(ip, port)

    def disconnect(self) -> None:
        """Desconecta do servidor."""

        if self.__network is not None:
            self.__network.disconnect()
            self.__network = None

    def init(self) -> None:
        """Inicializa o jogo."""

        self.__state.init()

    def update(self, dt: float) -> None:
        """Atualiza o jogo.

        Args:
            dt (float): Delta time. Tempo desde o último frame.
        """

        self.__state.update(dt)

    def update_server(self) -> None:
        """Atualiza o servidor."""

        self.__state.update_server()

    def draw(self) -> None:
        """Desenha o jogo."""

        self.__state.draw(self._surface)
