import pygame

from assets.components import Text, Button, TextInput, TempText
from core.graphics import Gfx
from .party import Party
from .state import State


class Host(State):
    def __init__(self, client):
        super().__init__(client)
        self.__cards = [
            pygame.transform.rotate(Gfx.WORLD_CARD, 15),
            pygame.transform.rotate(Gfx.BACK_CARD, -15)
        ]

    def init(self):
        cx = self._client.width // 2
        cy = self._client.height // 2

        self._client.add_component(
            Text("Host a LAN match", cx, 60, font_size=72, align="center"))

        self._client.add_component(
            Text("Nickname:", cx, 215, font_size=35, align="center"))
        self._client.add_component(
            TextInput(cx, 260, 300, 50, font_size=30,
                      max_length_input=16,
                      text_align="center", font_color="white", background_color="#a30f17",
                      border_color="#8c0d13", border_width=3, border_radius=5, align="center"),
            id="nickname")

        self._client.add_component(
            Text("Port:", cx, 310, font_size=35, align="center"))
        self._client.add_component(
            TextInput(cx, 355, 300, 50, font_size=30,
                      max_length_input=5, default="25565", numeric=True,
                      text_align="center", font_color="white", background_color="#a30f17",
                      border_color="#8c0d13", border_width=3, border_radius=5, align="center"),
            id="port")

        self._client.add_component(
            Button("> Start Match <", cx, 445, width=300, height=50,
                   font_size=40, align="center", animation="up",
                   on_click=self.__host_server))

        self._client.add_component(
            Button("< Back", 10, 560, height=30, font_size=32, on_click=self._client.pop_state))

    def __host_server(self, button: Button):
        nickname = self._client.get_component("nickname").text.strip()
        port = self._client.get_component("port").text

        if not self.__check_nickname(nickname):
            if self._client.get_component("error1") is not None: # remove the component if it already exists
                self._client.pop_component("error1")

            self._client.add_component(
                TempText("Nickname invalid", self._client.width // 2, 550, 3000,
                         font_size=30, align="center"), id="error1")
            return

        if not self._client.check_port("localhost", port):
            if self._client.get_component("error3") is not None:
                self._client.pop_component("error3")

            self._client.add_component(
                TempText("Port is already in use", self._client.width // 2, 550, 3000,
                         font_size=30, align="center"), id="error3")
            print("port is already in use")
            return

        self._client.host_server(port)
        pygame.time.wait(500)  # Espera o servidor iniciar
        self._client.connect("localhost", port)

        self._client.state = Party(self._client)

    def __check_nickname(self, nickname: str) -> bool:
        return 3 < len(nickname) <= 16

    def update_server(self):
        pass

    def draw(self, surface: pygame.Surface):
        surface.blit(Gfx.BACKGROUND, (0, 0))
        surface.blit(self.__cards[0], (40, 200))
        surface.blit(self.__cards[1], (610, 250))

