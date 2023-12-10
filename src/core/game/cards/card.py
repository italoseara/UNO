import abc
import pygame
from typing import Any

from core.graphics import Resources


class CardColor:
    RED = "red"
    BLUE = "blue"
    GREEN = "green"
    YELLOW = "yellow"
    WILD = "wild"


class Card(metaclass=abc.ABCMeta):
    """Classe base para cartas do jogo."""

    _images_cache: dict[str, pygame.Surface] = {}

    def __init__(self, color: str, value: str):
        self._color = color
        self._value = value

    @property
    def color(self) -> str:
        return self._color

    @color.setter
    def color(self, color: str) -> None:
        self._color = color

    @property
    def value(self) -> str:
        return self._value

    @property
    def name(self) -> str:
        return f"{self._color}-{self._value}"

    @property
    def image(self) -> pygame.Surface:
        if self.name not in self._images_cache:
            self._images_cache[self.name] = self.load_image()
        return self._images_cache[self.name]

    def load_image(self):
        img = Resources.CARDS[self._color][self._value + ".png"]
        return pygame.transform.scale(img, (int(img.get_width() * 3.5), int(img.get_height() * 3.5)))

    @abc.abstractmethod
    def play(self, match: Any, player_id: int):
        pass
