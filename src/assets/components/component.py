import pygame


class Component:
    def on_keydown(self, event: pygame.event):
        pass

    def update(self, dt: float):
        pass

    def draw(self, surface: pygame.Surface):
        pass
