import pygame
from .component import Component


class Text(Component):
    def __init__(self,
                 text: str,
                 x: int, y: int,
                 font: str = "ThaleahFat",
                 font_size: int = 12,
                 font_color: tuple[int, int, int] | str = "white",
                 align: str = "topleft"):
        # Texto
        self._text = text
        self._font = pygame.font.Font(f"./src/assets/fonts/{font}.ttf", font_size)
        self._font_color = font_color

        # Posição
        self._x = x
        self._y = y
        self._align = align

    def update(self, dt: float):
        pass

    def draw(self, surface: pygame.Surface):
        text = self._font.render(self._text, True, self._font_color)
        text_rect = text.get_rect()

        if self._align == "topleft":
            text_rect.topleft = (self._x, self._y)
        elif self._align == "center":
            text_rect.center = (self._x, self._y)

        surface.blit(text, text_rect)
