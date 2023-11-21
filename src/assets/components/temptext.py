import pygame
from .text import Text


class TempText(Text):
    def __init__(self,
                 text: str,
                 x: int, y: int,
                 lifespan: int = 1000,
                 font: str = "ThaleahFat",
                 font_size: int = 12,
                 font_color: tuple[int, int, int] | str = "white",
                 align: str = "topleft"):
        super().__init__(text, x, y, font, font_size, font_color, align)

        # Tempo de exibição
        self.__lifespan = lifespan

        # Tempo desde o início
        self.__init_time = pygame.time.get_ticks()

    @property
    def is_expired(self) -> bool:
        return pygame.time.get_ticks() - self.__init_time > self.__lifespan
