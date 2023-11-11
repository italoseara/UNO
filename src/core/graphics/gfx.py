import random
import pygame
import os


class Gfx:
    LOGO = pygame.image.load("src/assets/images/logo.png")
    MENU_BACKGROUND = pygame.image.load("src/assets/images/background/menu.png")
    CREDITS_BACKGROUND = pygame.image.load("src/assets/images/background/credits.png")

    @staticmethod
    def random_card() -> pygame.Surface:
        files = os.listdir("src/assets/images/cards")
        file = random.choice(files)

        # Load image with 500% scale
        image = pygame.image.load(f"src/assets/images/cards/{file}")
        image = pygame.transform.scale(image, (int(image.get_width() * 5), int(image.get_height() * 5)))

        return image
