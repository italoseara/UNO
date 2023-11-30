import pygame

from core.connection import Network


class State:
    """Classe base para os estados do jogo."""

    def __init__(self, client):
        from core.client import Client

        self._client: Client = client

    def init(self):
        """Inicializa o estado. Pode ser chamado várias vezes a fim de reiniciar o estado."""
        pass

    def update(self, dt: float):
        """Atualiza o estado.

        Args:
            dt (float): Delta time. Tempo desde o último frame.
        """
        pass

    def update_server(self, network: Network):
        """Atualiza o servidor."""
        pass

    def draw(self, surface: pygame.Surface):
        """Desenha o estado.

        Args:
            surface (pygame.Surface): Superfície onde o estado será desenhado.
        """
        pass
