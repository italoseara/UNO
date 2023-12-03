import random
import pygame
from util import Queue
#from core.graphics import Resources

from .cards import (
    Card, CardColor, NumberCard,
    DrawTwoCard, SkipCard, ReverseCard,
    WildCard, WildDrawFourCard
)


class Deck(Queue[Card]):
    """Classe que representa o baralho do jogo. Essencialmente, uma fila de cartas,
    pois as cartas são retiradas do topo e colocadas embaixo do baralho."""

    _queue: list[Card]

    def __init__(self):
        super().__init__()
        
        for color in [CardColor.RED, CardColor.GREEN, CardColor.BLUE, CardColor.YELLOW]:
            for number in range(10):
                for _ in range(2):
                    self._queue.append(NumberCard(color=color, value=str(number)))

            for _ in range(2):
                self._queue.append(DrawTwoCard(color=color))
                self._queue.append(SkipCard(color=color))
                self._queue.append(ReverseCard(color=color))

        for _ in range(4):
            self._queue.append(WildCard())
            self._queue.append(WildDrawFourCard())

        self.shuffle()

    def shuffle(self):
        """Embaralha o baralho"""

        random.shuffle(self._queue)
