import random
import pygame
import os


class Resources:
    """Classe de recursos gráficos, como imagens."""

    LOGO = pygame.image.load("src/assets/images/logo.png")
    BACKGROUND = pygame.image.load("src/assets/images/background/credits.png")
    MENU_BACKGROUND = pygame.image.load("src/assets/images/background/menu.png")
    WORLD_CARD = pygame.image.load("src/assets/images/world.png")
    BACK_CARD = pygame.image.load("src/assets/images/back.png")

    @staticmethod
    def random_card() -> pygame.Surface:
        """Seleciona uma carta aleatória.

        Returns:
            Surface: Imagem da carta 500% maior que a imagem original.
        """

        files = os.listdir("src/assets/images/cards")
        file = random.choice(files)

        # Load image with 500% scale
        image = pygame.image.load(f"src/assets/images/cards/{file}")
        image = pygame.transform.scale(image, (int(image.get_width() * 5), int(image.get_height() * 5)))

        return image
