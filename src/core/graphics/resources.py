import random
import pygame
import os


class Resources:
    """Classe de recursos gráficos, como imagens."""

    LOGO = pygame.image.load("src/assets/images/logo.png")
    BACKGROUND = pygame.image.load("src/assets/images/background/credits.png")
    MENU_BACKGROUND = pygame.image.load("src/assets/images/background/menu.png")
    CARD_WORLD_RESIZED = pygame.image.load("src/assets/images/resized/world.png")
    CARD_BACK_RESIZED = pygame.image.load("src/assets/images/resized/back.png")
    CARD_BACK = pygame.image.load("src/assets/images/cards/back.png")

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
