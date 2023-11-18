import pygame
from .text import Text

class TempText(Text):

    def __init__(self,
                 text: str,
                 x: int, y: int,
                 time: int,
                 font: str = "ThaleahFat",
                 font_size: int = 12,
                 font_color: tuple[int, int, int] | str = "white",
                 align: str = "topleft"):

        super().__init__(text, x, y, font, font_size, font_color, align)

        # Tempo de exibição
        self.__time = time

        # Tempo desde o início
        self.__init_time = pygame.time.get_ticks()


    def draw(self, surface: pygame.Surface):
        # Tempo atual
        current_time = pygame.time.get_ticks()

        if current_time - self.__init_time > self.__time:
            return

        super().draw(surface)
