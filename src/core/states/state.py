import pygame


class State:
    def __init__(self, client):
        """Inicializa o estado.

        Args:
            client (Client): Cliente.
        """

        self._client = client

    def init(self):
        """Inicializa o estado. Pode ser chamado várias vezes a fim de reiniciar o estado."""
        pass

    def update(self, dt: float):
        """Atualiza o estado.

        Args:
            dt (float): Delta time. Tempo desde o último frame.
        """
        pass

    def update_server(self):
        """Atualiza o servidor."""
        pass

    def draw(self, surface: pygame.Surface):
        """Desenha o estado.

        Args:
            surface (pygame.Surface): Superfície onde o estado será desenhado.
        """
        pass
