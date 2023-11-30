import random
from .cards import (
    Card, CardColor, NumberCard,
    DrawTwoCard, SkipCard, ReverseCard,
    WildCard, WildDrawFourCard
)


class Deck:
    """Classe que representa o baralho do jogo. Essencialmente, uma fila de cartas,
    pois as cartas são retiradas do topo e colocadas embaixo do baralho."""

    __cards: list[Card]

    def __init__(self):
        self.__cards = []
        for color in [CardColor.RED, CardColor.GREEN, CardColor.BLUE, CardColor.YELLOW]:
            for number in range(10):
                for _ in range(2):
                    self.__cards.append(NumberCard(color=color, value=str(number)))

            for _ in range(2):
                self.__cards.append(DrawTwoCard(color=color))
                self.__cards.append(SkipCard(color=color))
                self.__cards.append(ReverseCard(color=color))

        for _ in range(4):
            self.__cards.append(WildCard())
            self.__cards.append(WildDrawFourCard())

        self.shuffle()

    def shuffle(self):
        """Embaralha o baralho"""

        random.shuffle(self.__cards)

    def draw_card(self) -> Card:
        """Retira uma carta do topo do baralho"""

        return self.__cards.pop()

    def push(self, card: Card) -> None:
        """Coloca uma carta no fundo do baralho"""

        self.__cards.insert(0, card)
