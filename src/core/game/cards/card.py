import pygame

from core.graphics import Resources


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
        if self._name not in self._images_cache:
            self._images_cache[self._name] = self.load_image()
        return self._images_cache[self._name]

    def load_image(self):
        img = Resources.CARDS[self._color][self._value + ".png"]
        return pygame.transform.scale(img, (int(img.get_width() * 3.5), int(img.get_height() * 3.5)))

    def play(self, game):
        pass
