from .cards.card import Card


class Player:
    __id: int
    __name: str
    __hand: list[Card]

    def __init__(self, id: int, name: str):
        self.__id = id
        self.__name = name
        self.__hand = []

    @property
    def id(self) -> int:
        return self.__id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def hand(self) -> list[Card]:
        return self.__hand

    def add_card(self, card: Card) -> None:
        """Adiciona uma carta à mão do jogador

        Args:
            card (Card): Carta a ser adicionada
        """

        self.__hand.append(card)

    def remove_card(self, index: int) -> None:
        """Remove uma carta da mão do jogador

        Args:
            index (int): Índice da carta a ser removida
        """

        self.__hand.pop(index)