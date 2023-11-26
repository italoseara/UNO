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
