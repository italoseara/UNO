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
        self.text = text
        self.font = pygame.font.Font(f"src/assets/fonts/{font}.ttf", font_size)
        self.font_color = font_color

        # Posição
        self.x = x
        self.y = y

    def update(self, dt: float):
        pass

    def draw(self, surface: pygame.Surface):
        text = self.font.render(self.text, True, self.font_color)
        text_rect = text.get_rect()

        text_rect.center = (
            self.x + text_rect.width / 2,
            self.y + text_rect.height / 2
        )

        surface.blit(text, text_rect)
