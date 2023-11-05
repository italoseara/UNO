import pygame

from core.connection import Network
from .state import State


class Join(State):

    def init(self):
        self.client.connect("localhost", 5555)

    def update(self, dt: float):
        pass

    def update_server(self, network: Network):
        pass

    def draw(self, surface: pygame.Surface):
        surface.fill((255, 255, 255))
