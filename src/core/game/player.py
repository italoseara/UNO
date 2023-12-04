from .cards.card import Card


class Player:
    __id: int
    __name: str
    __hand: list[Card]
    __selecting_color: bool
    __selected_color: str | None

    def __init__(self, id: int, name: str):
        self.__id = id
        self.__name = name
        self.__hand = []

        self.__selecting_color = False
        self.__selected_color = None

    @property
    def id(self) -> int:
        return self.__id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def hand(self) -> list[Card]:
        return self.__hand

    @property
    def selecting_color(self) -> bool:
        return self.__selecting_color

    @selecting_color.setter
    def selecting_color(self, value: bool) -> None:
        self.__selecting_color = value

    def add_card(self, card: Card) -> None:
        """Adiciona uma carta à mão do jogador

        Args:
            card (Card): Carta a ser adicionada
        """

        self.__hand.append(card)

    def remove_card(self, index: int) -> Card:
        """Remove uma carta da mão do jogador

        Args:
            index (int): Índice da carta a ser removida
        """

        return self.__hand.pop(index)
