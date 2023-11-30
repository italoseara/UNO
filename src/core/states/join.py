import pygame

from core.graphics import Resources
from core.connection import Network
from assets.components import Text, Button, TextInput, WarningText

from .party import Party
from .state import State


class Join(State):
    __cards: list[pygame.Surface]

    def __init__(self, client):
        super().__init__(client)
        self.__cards = [
            pygame.transform.rotate(Resources.CARD_BACK_RESIZED, 15),
            pygame.transform.rotate(Resources.CARD_WORLD_RESIZED, -15)
        ]

    def init(self):
        cx = self._client.width // 2
        cy = self._client.height // 2

        self._client.add_component(
            Text("Join a LAN match", cx, 60, font_size=72, align="center"))

        self._client.add_component(
            Text("Nickname:", cx, 150, font_size=35, align="center"))
        self._client.add_component(
            TextInput(cx, 195, 300, 50, font_size=30,
                      max_length_input=10,
                      text_align="center", font_color="white", background_color="#a30f17",
                      border_color="#8c0d13", border_width=3, border_radius=5, align="center"),
            id="nickname")

        self._client.add_component(
            Text("IP:", cx, 245, font_size=35, align="center"))
        self._client.add_component(
            TextInput(cx, 290, 300, 50, font_size=30,
                      text_align="center", font_color="white", background_color="#a30f17",
                      border_color="#8c0d13", border_width=3, border_radius=5, align="center", default="localhost"),
            id="ip")

        self._client.add_component(
            Text("Port:", cx, 340, font_size=35, align="center"))
        self._client.add_component(
            TextInput(cx, 385, 300, 50, font_size=30,
                      max_length_input=5, numeric=True,
                      text_align="center", font_color="white", background_color="#a30f17",
                      border_color="#8c0d13", border_width=3, border_radius=5, align="center", default="25565"),
            id="port")

        self._client.add_component(
            Button("> Join Match <", cx, 475, width=300, height=50,
                   font_size=40, align="center", animation="up",
                   on_click=self.__join_server))

        self._client.add_component(
            Button("< Back", 10, 560, height=30, font_size=32, on_click=self._client.pop_state))

    def __join_server(self, button: Button):
        nickname = self._client.get_component("nickname").text.strip()
        port = self._client.get_component("port").text
        ip = self._client.get_component("ip").text

        if not self.__check_nickname(nickname):
            self._client.add_component(
                WarningText("Invalid Nickname", self._client.width // 2, 550,
                            font_size=30, align="center"))
            return

        if not self.__check_ip(ip):
            self._client.add_component(
                WarningText("Invalid IP Address", self._client.width // 2, 550,
                            font_size=30, align="center"))
            return

        if not Network.server_running(ip, port):
            self._client.add_component(
                WarningText("Server not found", self._client.width // 2, 550,
                            font_size=30, align="center"))
            return

        self._client.connect(ip, port)
        pygame.time.wait(100)

        # Tenta se conectar ao servidor 10 vezes
        result = None
        for _ in range(10):
            result = self._client.send({"type": "JOIN", "nickname": nickname})
            if result is not None:
                break

        # Se o servidor estiver cheio, mostra um aviso
        if result == "full":
            self._client.disconnect()
            self._client.add_component(
                WarningText("Match is full", self._client.width // 2, 550,
                            font_size=30, align="center"))
            return

        # Se o nickname já estiver em uso, mostra um aviso
        if result == "nickname":
            self._client.disconnect()
            self._client.add_component(
                WarningText("Nickname already in use", self._client.width // 2, 550,
                            font_size=30, align="center"))
            return

        # Se o servidor não estiver respondendo, mostra um aviso
        if result is None:
            self._client.disconnect()
            self._client.add_component(
                WarningText("Server not responding", self._client.width // 2, 550,
                            font_size=30, align="center"))
            return

        self._client.state = Party(self._client)

    @staticmethod
    def __check_nickname(nickname: str) -> bool:
        return 3 <= len(nickname) <= 10

    @staticmethod
    def __check_ip(ip: str) -> bool:
        return ip != ""

    def update(self, dt: float):
        pass

    def update_server(self, network: Network):
        pass

    def draw(self, surface: pygame.Surface):
        surface.blit(Resources.BACKGROUND, (0, 0))
        surface.blit(self.__cards[0], (40, 200))
        surface.blit(self.__cards[1], (610, 250))
