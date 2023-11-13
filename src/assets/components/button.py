import pygame
from .component import Component


class Button(Component):
    def __init__(self,
                 text: str,
                 x: int, y: int,
                 width: int | str = "auto",
                 height: int | str = "auto",
                 text_align: str = "center",
                 align: str = "topleft",
                 font: str = "ThaleahFat",
                 font_size: int = 20,
                 font_color: tuple[int, int, int] | str = "white",
                 hover_color: tuple[int, int, int] | str = "gray",
                 background_color: tuple[int, int, int] | str | None = None,
                 border_radius: int = 0,
                 border_width: int = 0,
                 border_color: tuple[int, int, int] | str = "black",
                 animation: str = "right",
                 on_click: callable = None):
        # Texto
        self.__text = text
        self.__text_align = text_align
        self.__font = pygame.font.Font(f"./src/assets/fonts/{font}.ttf", font_size)
        self.__font_color = font_color
        self.__hover_color = hover_color

        # Posição e tamanho
        self.__x = x
        self.__y = y
        self.__width = self.__font.size(text)[0] + 20 if width == "auto" else width
        self.__height = self.__font.size(text)[1] - 20 if height == "auto" else height
        self.__align = align

        # Botão
        self.__rect = pygame.Rect((self.__x, self.__y), (self.__width, self.__height))
        self.__background_color = background_color

        # Borda
        self.__border = pygame.Rect((self.__x, self.__y), (self.__width, self.__height))
        self.__border_color = border_color
        self.__border_width = border_width
        self.__border_radius = border_radius

        # Animação ao passar o mouse
        self.__current_x = x
        self.__current_y = y
        self.__current_color = pygame.Color(font_color)
        self.__animation = animation

        # Função a ser executada
        self.__on_click = on_click

        # Verifica se o botão está sendo pressionado
        self.__is_pressing = False

    @property
    def text(self) -> str:
        return self.__text

    def __set_pos(self, x: int, y: int):
        # Muda a posição do botão gradualmente
        self.__current_x += 0.1 * (x - self.__current_x)
        self.__current_y += 0.1 * (y - self.__current_y)

        if self.__align == "topleft":
            self.__rect.topleft = (self.__current_x, self.__current_y)
            self.__border.topleft = (self.__current_x, self.__current_y)
        elif self.__align == "center":
            self.__rect.center = (self.__current_x, self.__current_y)
            self.__border.center = (self.__current_x, self.__current_y)

    def __set_color(self, color: tuple[int, int, int] | str):
        self.__current_color = self.__current_color.lerp(color, 0.1)

    def update(self, dt: float):
        if self.__on_click is None:
            return

        if not pygame.mouse.get_pressed()[0]:
            self.__is_pressing = False

        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.__rect.collidepoint(mouse_x, mouse_y):
            if self.__animation == "right":
                self.__set_pos(self.__x + 15, self.__y)
            elif self.__animation == "left":
                self.__set_pos(self.__x - 15, self.__y)
            elif self.__animation == "up":
                self.__set_pos(self.__x, self.__y - 10)
            elif self.__animation == "down":
                self.__set_pos(self.__x, self.__y + 10)

            self.__set_color(self.__hover_color)

            if pygame.mouse.get_pressed()[0] and not self.__is_pressing:
                if self.__on_click is not None:
                    self.__on_click(self)
                self.__is_pressing = True
        else:
            self.__set_pos(self.__x, self.__y)
            self.__set_color(self.__font_color)

    def on_keydown(self, event: pygame.event):
        pass

    def draw(self, surface: pygame.Surface):
        # Desenha o botão
        if self.__background_color is not None:
            pygame.draw.rect(surface, self.__background_color, self.__rect, border_radius=self.__border_radius)

        # Desenha a borda
        if self.__border_width > 0:
            pygame.draw.rect(surface, self.__border_color, self.__border,
                             border_radius=self.__border_radius, width=self.__border_width)

        # Desenha o texto
        text = self.__font.render(self.__text, True, self.__current_color)
        txt_rect = text.get_rect()

        x = self.__current_x
        y = self.__current_y

        # Ajusta a posição do texto
        if self.__align == "topleft":
            if self.__text_align == "center":
                x += self.__width // 2
                y += self.__height // 2
            elif self.__text_align == "left":
                x += 10
                y += self.__height // 2
        if self.__align == "center":
            if self.__text_align == "left":
                x -= self.__width // 2 - 10

        if self.__text_align == "center":
            txt_rect.center = (x, y)
        elif self.__text_align == "left":
            txt_rect.midleft = (x, y)

        surface.blit(text, txt_rect)  # Desenha o texto na superfície do botão
