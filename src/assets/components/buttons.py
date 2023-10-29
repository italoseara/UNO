import pygame

class Button:

    def __init__(self, x: int, y: int, text: str, color: tuple[int,int,int], width: int, height: int, font = pygame.font.SysFont("arial", 10)):
        self.x = x
        self.y = y
        self.text = font.render(text, True, "white")    # achei melhor renderizar o texto logo na inicialização do botão
        self.color = color
        self.width = width
        self.height = height
        self.rect = pygame.Rect((self.x, self.y), (self.width, self.height))    # cria um obj retangulo


    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(surface, self.color, self.rect, border_radius= 10)
        txtRect = self.text.get_rect()                                          # cria um retagulo para ser a superficie do texto
        txtRect.center = ((self.x + self.width/2), (self.y + self.height/2))    # centraliza o texto conforme as
                                                                                # coordenadas do botão

    def update(self, dt: float):
        pass

