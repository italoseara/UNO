import pygame
from .component import Component


class Button(Component):
    def __init__(self,
                 text: str,
                 x: int, y: int,
                 width: int | str = "auto",
                 height: int | str = "auto",
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
        # Texto
        self.text = text
        self.text_align = text_align
        self.font = pygame.font.Font(f"src/assets/fonts/{font}.ttf", font_size)
        self.font_color = font_color
        self.hover_color = hover_color

        # Posição e tamanho
        self.x = x
        self.y = y
        self.width = self.font.size(text)[0] + 20 if width == "auto" else width
        self.height = self.font.size(text)[1] - 20 if height == "auto" else height

        # Botão
        self.rect = pygame.Rect((self.x, self.y), (self.width, self.height))
        self.background_color = background_color

        # Borda
        self.border = pygame.Rect((self.x, self.y), (self.width, self.height))
        self.border_color = border_color
        self.border_width = border_width
        self.border_radius = border_radius

        # Animação ao passar o mouse
        self.__current_x = x
        self.__current_y = y
        self.__current_color = pygame.Color(font_color)

        # Função a ser executada
        self.__on_click = on_click

        # Variáveis locais
        self.__is_pressing = False

    def set_pos(self, x: int, y: int):
        # Muda a posição do botão gradualmente
        self.__current_x += 0.1 * (x - self.__current_x)
        self.__current_y += 0.1 * (y - self.__current_y)

        self.rect.x = self.__current_x
        self.rect.y = self.__current_y

        self.border.x = self.__current_x
        self.border.y = self.__current_y

    def set_color(self, color: tuple[int, int, int] | str):
        self.__current_color = self.__current_color.lerp(color, 0.1)

    def update(self, dt: float):
        if self.__on_click is None:
            return

        if not pygame.mouse.get_pressed()[0]:
            self.__is_pressing = False

        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_x, mouse_y):
            self.set_pos(self.x + 15, self.y)
            self.set_color(self.hover_color)

            if pygame.mouse.get_pressed()[0] and not self.__is_pressing:
                if self.__on_click is not None:
                    self.__on_click(self)
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
        text = self.font.render(self.text, True, self.__current_color)
        txt_rect = text.get_rect()

        if self.text_align == "center":
            txt_rect.center = (
                self.__current_x + self.width / 2,
                self.__current_y + self.height / 2
            )
        elif self.text_align == "left":
            txt_rect.midleft = (
                self.__current_x + 10,
                self.__current_y + self.height / 2
            )

        surface.blit(text, txt_rect)  # Desenha o texto na superfície do botão
