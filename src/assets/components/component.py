import pygame


class Component:
    """Classe base para os componentes do jogo."""

    def update(self, dt: float):
        """Atualiza o componente.

        Args:
            dt (float): Delta time. Tempo desde o último frame.
        """
        pass

    def on_keydown(self, event: pygame.event):
        """Evento de tecla pressionada.

        Args:
            event (pygame.event): Evento de tecla pressionada.
        """

    def draw(self, surface: pygame.Surface):
        """Desenha o componente.

        Args:
            surface (pygame.Surface): Superfície onde o componente será desenhado.
        """
        pass
