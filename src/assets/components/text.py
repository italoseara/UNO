import pygame
from .component import Component


class Text(Component):
    def __init__(self,
                 text: str,
                 x: int, y: int,
                 font: str = "ThaleahFat",
                 font_size: int = 12,
                 font_color: tuple[int, int, int] | str = "white"):
        # Texto
        self.__text = text
        self.__font = pygame.font.Font(f"src/assets/fonts/{font}.ttf", font_size)
        self.__font_color = font_color

        # Posição
        self.__x = x
        self.__y = y

    def update(self, dt: float):
        pass

    def draw(self, surface: pygame.Surface):
        text = self.__font.render(self.__text, True, self.__font_color)
        text_rect = text.get_rect()

        text_rect.center = (
            self.__x + text_rect.width / 2,
            self.__y + text_rect.height / 2
        )

        surface.blit(text, text_rect)
