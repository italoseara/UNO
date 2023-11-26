import pygame


class CardColor:
    RED = "red"
    BLUE = "blue"
    GREEN = "green"
    YELLOW = "yellow"
    WILD = "wild"


class Card:
    """Classe base para cartas do jogo."""

    _images_cache: dict[str, pygame.Surface] = {}

    def __init__(self, color: str, value: str):
        self._color = color
        self._value = value

        self._name = f"{self._color}-{self._value}"
        self._image_path = f"src/assets/images/cards/{self._color}/{self._value}.png"

    @property
    def color(self) -> str:
        return self._color

    @property
    def name(self) -> str:
        return self._name

    @property
    def image(self) -> pygame.Surface:
        return self._images_cache.setdefault(self._name, self.load_image())

    def load_image(self):
        img = pygame.image.load(self._image_path)
        return pygame.transform.scale(img, (int(img.get_width() * 3.5), int(img.get_height() * 3.5)))

    def play(self, game):
        pass
