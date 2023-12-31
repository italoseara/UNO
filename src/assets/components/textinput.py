import pygame
import pygame.locals
import pyperclip

from .component import Component


class TextInput(Component):

    def __init__(self, x: int, y: int,
                 width: int, height: int,
                 default: str = "",
                 max_length_input: int | str = "auto",
                 text_align: str = "center",
                 align: str = "topleft",
                 font: str = "ThaleahFat",
                 font_size: int = 32,
                 font_color: tuple[int, int, int] | str = "white",
                 background_color: tuple[int, int, int] | str | None = None,
                 border_radius: int = 0,
                 border_width: int = 0,
                 border_color: tuple[int, int, int] | str = "black",
                 numeric: bool = False):

        # Posição e tamanho da caixa de texto
        self.__x = x
        self.__y = y
        self.__width = width
        self.__height = height

        # Texto
        self.__text_align = text_align
        self.__text_color = font_color
        self.__text_font = pygame.font.Font(f"./src/assets/fonts/{font}.ttf", font_size)
        self.__max_length_input = max_length_input

        # Surface
        self.__rect = pygame.Rect((self.__x, self.__y), (self.__width, self.__height))
        if align == "center":
            self.__rect.center = (self.__x, self.__y)

        self.__background_color = background_color

        # Surface da caixa de texto
        self.__input_rect = pygame.Rect((self.__x, self.__y), (self.__width, self.__height))
        if align == "center":
            self.__input_rect.center = (self.__x, self.__y)

        self.__border_width = border_width
        self.__border_radius = border_radius
        self.__border_color = border_color

        # Guarda input de texto do user
        self.__user_input = default

        # Confere se a caixa de texto está em foco
        self.__on_focus = False

        # Limita o tipo de input
        self.__numeric = numeric

    @property
    def text(self) -> str | int:
        if self.__numeric:
            if self.__user_input == "":
                return 0
            return int(self.__user_input)
        return self.__user_input

    def on_keydown(self, event: pygame.event):
        if self.__on_focus:
            if event.key == pygame.K_BACKSPACE:  # Unicode gera caractere invalido se apertar backspace
                self.__user_input = self.__user_input[0:-1]
            if event.key == pygame.K_v and pygame.key.get_mods() & pygame.KMOD_CTRL:
                if self.__numeric and not pyperclip.paste().isnumeric(): # Verifica se o texto é um número (porta)
                    return
                if len(pyperclip.paste()) > self.__max_length_input: # Verifica se o texto é maior que o limite
                    self.__user_input = pyperclip.paste()[0:self.__max_length_input]
                    return
                self.__user_input += pyperclip.paste()
            elif event.unicode.isprintable():  # Verifica se o caractere é imprimível
                if self.__max_length_input == "auto" and self.__text_font.size(self.__user_input)[0] >= self.__width - 30:
                    return  # Não adiciona o input se o texto já estiver no limite da caixa de texto
                if self.__max_length_input == "auto" or len(self.__user_input) < self.__max_length_input:
                    if self.__numeric and not event.unicode.isnumeric():
                        return
                    self.__user_input += event.unicode  # Adiciona o input à string, seja numero ou letra

    def update(self, dt: float):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        if pygame.mouse.get_pressed()[0]:
            # Tira o foco da caixa de texto
            if not self.__input_rect.collidepoint(mouse_x, mouse_y):
                self.__on_focus = False

            # Põe o foco na caixa de texto
            if self.__input_rect.collidepoint(mouse_x, mouse_y):
                self.__on_focus = True

    def draw(self, surface: pygame.Surface):
        # Desenha o background
        if self.__background_color is not None:
            pygame.draw.rect(surface, self.__background_color, self.__rect, border_radius=self.__border_radius)

        # Desenha a surface do text_input
        if self.__border_width > 0:
            pygame.draw.rect(surface, self.__border_color, self.__input_rect,
                             border_radius=self.__border_radius, width=self.__border_width)

        # Coloca o input nas coordenadas da surface
        input_surface = self.__text_font.render(self.__user_input, True, self.__text_color)
        input_width, input_height = input_surface.get_size()

        # Coloca o input no centro da surface
        if self.__text_align == "center":
            surface.blit(input_surface, (
                self.__input_rect.x - input_width / 2 + self.__input_rect.w / 2,
                self.__input_rect.y - input_height / 2 + self.__input_rect.h / 2
            ))
        elif self.__text_align == "left":
            surface.blit(input_surface, (
                self.__input_rect.x + 10,
                self.__input_rect.y + self.__input_rect.h / 2 - input_height / 2
            ))

        # Auto resize
        self.__input_rect.w = max(self.__width, input_surface.get_width() + 20)
        self.__rect.w = self.__input_rect.w
        self.__rect.x = self.__input_rect.x
