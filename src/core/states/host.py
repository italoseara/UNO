from random import randint

import pygame

from assets.components import Text, Button, TextInput
from core.graphics import Gfx
from .party import Party
from .state import State


class Host(State):
    def init(self):
        cx = self._client.width // 2
        cy = self._client.height // 2

        self._client.add_component(
            Text("Host", cx, 60, font_size=72, align="center"))

        self._client.add_component(
            Button("Back", 10, 560, height=30, font_size=32, on_click=self._client.pop_state))

        self._client.add_component(
            TextInput(cx - 100, 250, 200, 50, font_size=30, max_length_input=10,
                      text_align="center", font_color="black", background_color="white", border_radius=15,
                      border_width=5, border_color="gray"),
            id="nickname")

        self._client.add_component(
            Text("Nickname", cx, 200, font_size=45, align="center"))

        self._client.add_component(
            Button("Host", cx - 90, 350, height=50, font_size=35,
                   on_click=self.__host_server))

    def __host_server(self, button: Button):
        port = randint(10000, 65535)
        nickname = self._client.get_component("nickname").text

        self._client.host_server(port)
        pygame.time.wait(500)
        self._client.connect("localhost", port)

        # self._client.send({"type": "join", "nickname": nickname})
        self._client.state = Party(self._client)

    def update(self, dt: float):
        pass

    def update_server(self):
        pass

    def draw(self, surface: pygame.Surface):
        surface.blit(Gfx.BACKGROUND, (0, 0))
