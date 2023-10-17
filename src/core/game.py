import pygame
from src.engine import Engine, on_event


class Game(Engine):
    width: int
    height: int
    fps: int

    surface: pygame.Surface
    clock: pygame.time.Clock
3
    @on_event(type_=pygame.KEYDOWN)
    def on_keydown(self, event: pygame.event.Event) -> None:
        print("Key pressed", event.key)

    def init(self) -> None:
        pass

    def update(self, dt: float) -> None:
        pass

    def draw(self) -> None:
        pass
