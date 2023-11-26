import threading
from typing import Any

import pygame

from core.game import Match
from core.states import State, Menu
from core.connection import Network, Server
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
    __server: Server | None
    __server_thread: threading.Thread | None

    def __init__(self):
        super().__init__(caption="UNO in Python")
        self.__state = Menu(self)
        self.__last_state = self.__state

        self.__network = None
        self.__server = None
        self.__server_thread = None

    @property
    def state(self) -> State:
        return self.__state

    @state.setter
    def state(self, state: State) -> None:
        self.clear_components()
        self.__last_state = self.__state
        self.__state = state
        self.__state.init()

    @on_event(pygame.QUIT)
    def on_quit(self, _) -> None:
        """Evento de saída do jogo."""

        self.disconnect()
        self.close_server()

    def pop_state(self, *_, **__) -> None:
        """Retorna ao estado anterior."""

        self.state = self.__last_state

    def send(self, data: dict[str, Any]) -> Match | None:
        """Envia dados para o servidor."""

        if self.__network is not None:
            return self.__network.send(data)

    def connect(self, ip: str, port: int) -> None:
        """Conecta ao servidor."""

        if self.__network is not None:
            self.__network.disconnect()

        self.__network = Network(ip, port)

    def host_server(self, port: int) -> None:
        if self.__server is not None:
            self.__server.stop()

        self.__server = Server("localhost", port)
        self.__server_thread = threading.Thread(target=self.__server.start)
        self.__server_thread.start()

    def disconnect(self) -> None:
        """Desconecta do servidor."""

        if self.__network is not None:
            self.__network.disconnect()
            self.__network = None

    def close_server(self) -> None:
        if self.__server is not None:
            self.__server.stop()
            self.__server = None

        if self.__server_thread is not None:
            self.__server_thread.join()
            self.__server_thread = None

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

        self.__state.update_server(self.__network)

    def draw(self) -> None:
        """Desenha o jogo."""

        self.__state.draw(self._surface)
