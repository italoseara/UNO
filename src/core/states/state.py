import pygame

from core.connection import Network


class State:
    def __init__(self, client):
        self.client = client

    def init(self):
        pass

    def update(self, dt: float):
        pass

    def update_server(self, network: Network):
        pass

    def draw(self, surface: pygame.Surface):
        pass
