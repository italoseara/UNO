import pygame
from .component import Component

class TempText(Component):

    def __init__(self,
                 text: str,
                 x: int, y: int,
                 time: int,
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

        # Tempo de exibição
        self.__time = time

        # Tempo desde o início
        self.__init_time = pygame.time.get_ticks()

    def update(self, dt: float):
        pass

    def draw(self, surface: pygame.Surface):
        # Tempo atual
        current_time = pygame.time.get_ticks()

        if current_time - self.__init_time > self.__time:
            return

        text = self.__font.render(self.__text, True, self.__font_color)
        text_rect = text.get_rect()

        if self.__align == "topleft":
            text_rect.topleft = (self.__x, self.__y)
        elif self.__align == "center":
            text_rect.center = (self.__x, self.__y)

        surface.blit(text, text_rect)

