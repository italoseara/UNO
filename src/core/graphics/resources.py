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

    # Carrega todas as cartas do jogo previamente (para evitar carregamento durante a partida)
    CARDS = {
        "blue": {file: pygame.image.load(f"src/assets/images/cards/blue/{file}")
                 for file in os.listdir("src/assets/images/cards/blue")},
        "green": {file: pygame.image.load(f"src/assets/images/cards/green/{file}")
                  for file in os.listdir("src/assets/images/cards/green")},
        "red": {file: pygame.image.load(f"src/assets/images/cards/red/{file}")
                for file in os.listdir("src/assets/images/cards/red")},
        "yellow": {file: pygame.image.load(f"src/assets/images/cards/yellow/{file}")
                   for file in os.listdir("src/assets/images/cards/yellow")},
        "wild": {file: pygame.image.load(f"src/assets/images/cards/wild/{file}")
                 for file in os.listdir("src/assets/images/cards/wild")}
    }

    @staticmethod
    def random_card() -> pygame.Surface:
        """Seleciona uma carta aleatória.

        Returns:
            Surface: Imagem da carta 500% maior que a imagem original.
        """

        color = random.choice(list(Resources.CARDS.keys()))
        image = random.choice(list(Resources.CARDS[color].values()))
        image = pygame.transform.scale(image, (int(image.get_width() * 5), int(image.get_height() * 5)))

        return image.convert_alpha()
