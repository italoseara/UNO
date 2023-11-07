import pygame

from .state import State


class Join(State):

    def init(self):
        try:
            self._client.connect("localhost", 5555)
        except ConnectionRefusedError:
            print("Server is not running")

            from .menu import Menu
            self._client.state = Menu(self._client)

    def update(self, dt: float):
        pass

    def update_server(self):
        pass

    def draw(self, surface: pygame.Surface):
        surface.fill((255, 255, 255))
