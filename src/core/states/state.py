import pygame


class State:
    def __init__(self, client):
        self._client = client

    def init(self):
        pass

    def update(self, dt: float):
        pass

    def update_server(self):
        pass

    def draw(self, surface: pygame.Surface):
        pass
