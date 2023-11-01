import pygame
from .component import Component


class Text_input(Component):

    def __init__(self, x: int, y: int,
                 width: int, height: int,
                 max_length_input: int = 10,
                 text_size: int = 10,
                 text_font: str = "Arial",
                 text_color: tuple[int, int, int] | str = "black",
                 background_color: tuple[int, int, int] | str | None = "grey",
                 border_radius: int = 0,
                 border_width: int = 0,
                 border_color: tuple[int, int, int] | str = "black"):

        # Posição e tamanho da caixa de texto
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        # Tamanho e cor da fonte
        self.text_font = pygame.font.Font(text_font, text_size)
        self.text_color = text_color
        
        # Máximo de caracteres no input
        self.max_length_input = max_length_input
        # Guarda input de texto do user
        self.user_input = ""

        # Confere se a caixa de texto está em foco
        self.on_focus = False

        # Surface da caixa de texto
        self.input_rect = pygame.Rect((self.x, self.y), (self.width, self.height))
        self.border_width = border_width
        self.background_color = background_color
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

        if self.on_focus:
            for event in pygame.event.get(): # Não sei se o loop é necessário, mas preferi pôr
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE: # Unicode gera caractere invalido se apertar backspace
                        self.user_input = self.user_input[0:-1]
                    else:
                        if len(self.user_input) < self.max_length_input:
                            self.user_input += event.unicode # Adiciona o input à string, se ainda tiver dentro da capacidade

    def draw(self, surface: pygame.Surface):
        # Desenha a surface do text_input
        pygame.draw.rect(surface, self.background_color, self.input_rect, self.border_width, self.border_radius)

        # Coloca o input nas coordenadas da surface
        input_surface = self.text_font.render(self.user_input, True, self.border_color)
        surface.blit(input_surface, (self.input_rect.x, self.input_rect.y)) # Falta centralizar o input
        self.input_rect.w = max(150, input_surface.get_width() + 10) # Se a caixa de input ficar pequena, se adapta
                                                                     # à largura do input
                                                                     # Não sei se será necessário