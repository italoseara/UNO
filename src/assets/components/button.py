import pygame
from .component import Component


class Button(Component):
    def __init__(self,
                 x: int, y: int,
                 width: int, height: int,
                 text: str,
                 text_align: str = "center",
                 font: str = "ThaleahFat",
                 font_size: int = 20,
                 font_color: tuple[int, int, int] | str = "white",
                 hover_color: tuple[int, int, int] | str = "gray",
                 background_color: tuple[int, int, int] | str | None = None,
                 border_radius: int = 0,
                 border_width: int = 0,
                 border_color: tuple[int, int, int] | str = "black",
                 on_click: callable = None):
        # Posição e tamanho
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        # Botão
        self.rect = pygame.Rect((self.x - self.width/2, self.y - self.height/2), (self.width, self.height))
        self.background_color = background_color

        # Borda
        self.border = pygame.Rect((self.x - self.width/2, self.y - self.height/2), (self.width, self.height))
        self.border_color = border_color
        self.border_width = border_width
        self.border_radius = border_radius

        # Texto
        self.text = text
        self.text_align = text_align
        self.font = pygame.font.Font(f"src/assets/fonts/{font}.ttf", font_size)
        self.font_color = font_color
        self.hover_color = hover_color

        # Função a ser executada
        self.on_click = on_click

        # Variáveis locais
        self.__is_pressing = False

        # Animation
        self.current_x = x
        self.current_y = y
        self.current_color = pygame.Color(font_color)

    def set_pos(self, x: int, y: int):
        # Muda a posição do botão gradualmente
        self.current_x += 0.1 * (x - self.current_x)
        self.current_y += 0.1 * (y - self.current_y)

        self.rect.x = self.current_x - self.width / 2
        self.rect.y = self.current_y - self.height / 2

        self.border.x = self.current_x - self.width / 2
        self.border.y = self.current_y - self.height / 2

    def set_color(self, color: tuple[int, int, int] | str):
        self.current_color = self.current_color.lerp(color, 0.1)

    def update(self, dt: float):
        if self.on_click is None:
            return

        if not pygame.mouse.get_pressed()[0]:
            self.__is_pressing = False

        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_x, mouse_y):
            self.set_pos(self.x + 15, self.y)
            self.set_color(self.hover_color)

            if pygame.mouse.get_pressed()[0] and not self.__is_pressing:
                if self.on_click is not None:
                    self.on_click(self)
                self.__is_pressing = True
        else:
            self.set_pos(self.x, self.y)
            self.set_color(self.font_color)

    def on_keydown(self, event: pygame.event):
        pass

    def draw(self, surface: pygame.Surface):
        # Desenha o botão
        if self.background_color is not None:
            pygame.draw.rect(surface, self.background_color, self.rect, border_radius=self.border_radius)

        # Desenha a borda
        if self.border_width > 0:
            pygame.draw.rect(surface, self.border_color, self.border,
                             border_radius=self.border_radius, width=self.border_width)

        # Desenha o texto
        text = self.font.render(self.text, True, self.current_color)
        txt_rect = text.get_rect()

        if self.text_align == "center":
            txt_rect.center = (self.current_x, self.current_y)
        elif self.text_align == "left":
            txt_rect.center = (self.current_x - self.width / 2 + txt_rect.w / 2 + self.border_width, self.current_y)
        surface.blit(text, txt_rect)  # Desenha o texto na superfície do botão
