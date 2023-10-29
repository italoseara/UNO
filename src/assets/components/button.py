import pygame
from .component import Component


class Button(Component):
    def __init__(self,
                 x: int, y: int,
                 width: int, height: int,
                 text: str,
                 text_size: int = 20,
                 text_font: str = "Arial",
                 text_color: tuple[int, int, int] | str = "black",
                 background_color: tuple[int, int, int] | str | None = "white",
                 border_radius: int = 0,
                 border_width: int = 0,
                 border_color: tuple[int, int, int] | str = "black",
                 action: callable = None):
        # Posição e tamanho
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        # Botão
        self.rect = pygame.Rect(
            (self.x + border_width, self.y + border_width),
            (self.width - border_width * 2, self.height - border_width * 2))
        self.background_color = background_color
        self.border_radius = border_radius

        # Borda
        self.border = pygame.Rect((self.x, self.y), (self.width, self.height))
        self.border_color = border_color
        self.border_width = border_width

        # Texto
        self.text = pygame.font.SysFont(text_font, text_size).render(text, True, text_color)

        # Função a ser executada
        self.action = action

        # Variáveis locais
        self.__is_pressing = False

    def update(self, dt: float):
        if self.action is None:
            return

        if not pygame.mouse.get_pressed()[0]:
            self.__is_pressing = False
            return

        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_x, mouse_y) and pygame.mouse.get_pressed()[0] and not self.__is_pressing:
            self.action()
            self.__is_pressing = True

    def draw(self, surface: pygame.Surface):
        # Desenha o botão
        pygame.draw.rect(surface, self.border_color, self.border,
                         border_radius=self.border_radius, width=self.border_width)
        if self.background_color is not None:
            pygame.draw.rect(surface, self.background_color, self.rect, border_radius=self.border_radius)

        # Desenha o texto
        txt_rect = self.text.get_rect()
        txt_rect.center = ((self.x + self.width / 2), (self.y + self.height / 2))
        surface.blit(self.text, txt_rect)  # Desenha o texto na superfície do botão
