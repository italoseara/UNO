
import pygame

from assets.components import Text, Button, TextInput
from core.graphics import Gfx
from .party import Party
from .state import State


class Join(State):
    def __init__(self, client):
        super().__init__(client)
        self.__cards = [
            pygame.transform.rotate(Gfx.BACK_CARD, 15),
            pygame.transform.rotate(Gfx.WORLD_CARD, -15)
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
                      max_length_input=16,
                      text_align="center", font_color="white", background_color="#a30f17",
                      border_color="#8c0d13", border_width=3, border_radius=5, align="center"),
            id="nickname")

        self._client.add_component(
            Text("IP:", cx, 245, font_size=35, align="center"))
        self._client.add_component(
            TextInput(cx, 290, 300, 50, font_size=30,
                      text_align="center", font_color="white", background_color="#a30f17",
                      border_color="#8c0d13", border_width=3, border_radius=5, align="center"),
            id="ip")

        self._client.add_component(
            Text("Port:", cx, 340, font_size=35, align="center"))
        self._client.add_component(
            TextInput(cx, 385, 300, 50, font_size=30,
                      max_length_input=5, numeric=True,
                      text_align="center", font_color="white", background_color="#a30f17",
                      border_color="#8c0d13", border_width=3, border_radius=5, align="center"),
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
            print("nickname is invalid")
            return

        if not self._client.check_port(ip, port):
            print("server not found")
            return

        self._client.connect("localhost", port)
        self._client.state = Party(self._client)

    def __check_nickname(self, nickname: str) -> bool:
        return 3 < len(nickname) <= 16

    def update(self, dt: float):
        pass

    def update_server(self):
        pass

    def draw(self, surface: pygame.Surface):
        surface.blit(Gfx.BACKGROUND, (0, 0))
        surface.blit(self.__cards[0], (40, 200))
        surface.blit(self.__cards[1], (610, 250))
