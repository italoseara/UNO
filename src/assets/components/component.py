import pygame


class Component:
    def update(self, dt: float):
        pass

    def on_keydown(self, event: pygame.event):
        pass

    def draw(self, surface: pygame.Surface):
        pass
