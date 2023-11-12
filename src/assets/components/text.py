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
        self.__text = text
        self.__font = pygame.font.Font(f"./src/assets/fonts/{font}.ttf", font_size)
        self.__font_color = font_color

        # Posição
        self.__x = x
        self.__y = y
        self.__align = align

    def update(self, dt: float):
        pass

    def draw(self, surface: pygame.Surface):
        text = self.__font.render(self.__text, True, self.__font_color)
        text_rect = text.get_rect()

        if self.__align == "topleft":
            text_rect.topleft = (self.__x, self.__y)
        elif self.__align == "center":
            text_rect.center = (self.__x, self.__y)

        surface.blit(text, text_rect)
