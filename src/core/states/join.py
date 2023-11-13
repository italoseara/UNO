import pygame

from .party import Party
from .state import State
from core.graphics import Gfx
from assets.components import Button, Text, TextInput


class Join(State):
    def init(self):
        cx = self._client.width // 2
        cy = self._client.height // 2

        self._client.add_component(
            Text("Port", cx + 150, 200, font_size=50, align="center"))
        self._client.add_component(
            TextInput(cx + 50, 230, 200, 50, font_size=30, max_length_input=5,
                      text_align="center", font_color="black", background_color="white",
                      border_radius=15, border_width=5, border_color="gray", numeric=True),
            id="port")

        self._client.add_component(
            Text("Nickname", cx - 130, 200, font_size=50, align="center"))
        self._client.add_component(
            TextInput(cx - 230, 230, 200, 50, font_size=30, max_length_input=5,
                      text_align="center", font_color="black", background_color="white",
                      border_radius=15, border_width=5, border_color="gray", numeric=False),
            id="nickname")

        self._client.add_component(
            Button("Join server", cy, 350, height=50, font_size=35, on_click=self.__join_server))

        self._client.add_component(
            Button("< Back", 10, 560, height=30, font_size=32, on_click=self._client.pop_state))

    def __join_server(self, button: Button):
        port = self._client.get_component("port").text
        nickname = self._client.get_component("nickname").text

        try:
            self._client.connect("localhost", port)
        except ConnectionRefusedError:
            print("Server not found")

        # self._client.send({"type": "join", "nickname": nickname})
        self._client.state = Party(self._client)

    def update(self, dt: float):
        pass

    def update_server(self):
        pass

    def draw(self, surface: pygame.Surface):
        surface.blit(Gfx.BACKGROUND, (0, 0))
