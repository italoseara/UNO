import pygame


class CardColor:
    RED = "red"
    BLUE = "blue"
    GREEN = "green"
    YELLOW = "yellow"
    WILD = "wild"


class Card:
    """Classe das cartas comuns do jogo."""

    __images_cache: dict[str, pygame.Surface] = {}

    def __init__(self, color: str, value: str):
        self.__color = color
        self.__value = value

        self.__name = f"{self.__color}-{self.__value}"
        self.__image_path = f"src/assets/images/cards/{self.__color}/{self.__value}.png"

    @property
    def color(self) -> str:
        return self.__color

    @property
    def name(self) -> str:
        return self.__name

    @property
    def image(self) -> pygame.Surface:
        return self.__images_cache.setdefault(self.__name, self.load_image())

    def load_image(self):
        img = pygame.image.load(self.__image_path)
        img = pygame.transform.scale(img, (int(img.get_width() * 3.5), int(img.get_height() * 3.5)))
        return img
