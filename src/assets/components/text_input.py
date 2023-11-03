import pygame
from .component import Component


class Text_input(Component):

    def __init__(self, x: int, y: int,
                 width: int, height: int,
                 max_length_input: int = 10,
                 text_size: int = 12,
                 text_font: str = "Arial",
                 text_color: tuple[int, int, int] | str = "black",
                 background_color: tuple[int, int, int] | str | None = "white",
                 border_radius: int = 0,
                 border_width: int = 0,
                 border_color: tuple[int, int, int] | str = "black"):

        # Posição e tamanho da caixa de texto
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        # Tamanho e cor da fonte
        self.text_font = pygame.font.SysFont(text_font, text_size)
        self.text_color = text_color
        
        # Máximo de caracteres no input
        self.max_length_input = max_length_input
        # Guarda input de texto do user
        self.user_input = ""

        # Confere se a caixa de texto está em foco
        self.on_focus = False

        # Surface
        self.rect = pygame.Rect((self.x - self.width/2, self.y - self.height/2), (self.width, self.height))
        self.background_color = background_color

        # Surface da caixa de texto
        self.input_rect = pygame.Rect((self.x - self.width/2, self.y - self.height/2), (self.width, self.height))
        self.border_width = border_width
        self.border_radius = border_radius
        self.border_color = border_color

    def update(self, dt: float):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Tira o foco da caixa de texto
        if not self.input_rect.collidepoint(mouse_x, mouse_y) and pygame.mouse.get_pressed()[0]:
            self.on_focus = False

        # Põe o foco na caixa de texto
        if self.input_rect.collidepoint(mouse_x, mouse_y) and pygame.mouse.get_pressed()[0]:
            self.on_focus = True

    def on_keydown(self, event: pygame.event):
        if self.on_focus:
            if event.key == pygame.K_BACKSPACE:  # Unicode gera caractere invalido se apertar backspace
                self.user_input = self.user_input[0:-1]
            elif event.unicode.isprintable():  # Verifica se o caractere é imprimível
                if len(self.user_input) < self.max_length_input:
                    self.user_input += event.unicode  # Adiciona o input à string, se ainda tiver dentro da capacidade

    def draw(self, surface: pygame.Surface):
        # Desenha o background
        if self.background_color is not None:
            pygame.draw.rect(surface, self.background_color, self.rect, border_radius=self.border_radius)

        # Desenha a surface do text_input
        pygame.draw.rect(surface, self.border_color, self.input_rect,
                         border_radius=self.border_radius, width=self.border_width)

        # Coloca o input nas coordenadas da surface
        input_surface = self.text_font.render(self.user_input, True, self.text_color)
        input_width, input_height = input_surface.get_size()

        # Coloca o input no centro da surface
        surface.blit(input_surface, (
            self.input_rect.x - input_width/2 + self.input_rect.w/2,
            self.input_rect.y - input_height/2 + self.input_rect.h/2
        ))

        # Auto resize
        self.input_rect.w = max(150, input_surface.get_width() + 10)
        self.input_rect.x = self.x - self.input_rect.w/2
        self.rect.w = self.input_rect.w
        self.rect.x = self.input_rect.x
