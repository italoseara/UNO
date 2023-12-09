import pygame
from util import lerp

from .text import Text


class WarningText(Text):
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
        self.__created_at = pygame.time.get_ticks()

        # Animação
        self.__init_y = y
        self.__alpha = 255

    @property
    def is_expired(self) -> bool:
        return pygame.time.get_ticks() - self.__created_at > self.__lifespan

    def on_keydown(self, event: pygame.event):
        pass

    def update(self, dt: float):
        self._y = lerp(self._y, self.__init_y - 35, 0.02)
        self.__alpha = lerp(self.__alpha, 0, 0.02)

    def draw(self, surface: pygame.Surface):
        text, rect = self._render_text()
        text.set_alpha(self.__alpha)  # Define a transparência
        surface.blit(text, rect)
