import pygame
from typing import Self
from core.graphics import Resources
from core.game.match import Match
from core.game.cards import Card
from util import lerp


class InteractiveCard:
    def __init__(self, card, x, y) -> None:
        self.__card = card
        self.__x = x
        self.__y = y
        self.__original_x = x
        self.__original_y = y

    @property
    def card(self) -> Card:
        return self.__card

    def move(self, x: int = 0, y: int = 0) -> None:
        self.__x = lerp(self.__x, self.__original_x + x, 0.2)
        self.__y = lerp(self.__y, self.__original_y + y, 0.2)

    def draw(self, surface: pygame.Surface, image: pygame.Surface = None) -> None:
        surface.blit(image or self.__card.image, (self.__x, self.__y))

    def __is_hovering(self):
        x, y = pygame.mouse.get_pos()
        return self.__x <= x <= self.__x + self.__card.image.get_width() and \
               self.__y <= y <= self.__y + self.__card.image.get_height()

    def is_hovering(self, next_card: Self) -> bool:
        if next_card is None:
            return self.__is_hovering()

        return self.__is_hovering() and not next_card.__is_hovering()


class InteractiveCards:
    def __init__(self, client_id: int, client) -> None:
        self.__id = client_id
        self.__client = client
        self.__match = None
        self.__player = None

        self.__cards = []

        # Carta virada para baixo
        size = (int(Resources.CARD_BACK.get_width() * 3.5), int(Resources.CARD_BACK.get_height() * 3.5))
        self.__flipped_card = pygame.transform.scale(Resources.CARD_BACK, size).convert()

    def __update_cards(self) -> None:
        # TODO: Atualizar corretamente a lista de cartas
        if self.__player is None or self.__match is None:
            return

        hand = [card.name for card in self.__player.hand]
        interactive = [icard.card.name for icard in self.__cards]

        if hand != interactive:
            self.__cards.clear()

            max_space = -30
            max_dimension = 600

            card_dimension = self.__flipped_card.get_width()

            space = min(card_dimension + max_space, max_dimension // len(self.__player.hand))
            hand_dimension = (len(self.__player.hand) - 1) * space + card_dimension

            y = self.__client.height - self.__flipped_card.get_height() - 15

            for i, card in enumerate(self.__player.hand):
                x = self.__client.width // 2 - hand_dimension // 2 + i * space
                self.__cards.append(InteractiveCard(card, x, y))

    def __animate_cards(self) -> None:        
        for i, card in enumerate(self.__cards):
            next_card = self.__cards[i + 1] if i + 1 < len(self.__cards) else None
            
            card.move(y=-30 if card.is_hovering(next_card) else 0)

    def update(self, match: Match, dt: float) -> None:
        self.__match = match
        self.__player = self.__match.get_player(self.__id)

        # Atualiza a lista de cartas
        self.__update_cards()
        self.__animate_cards()

    def draw(self, surface: pygame.Surface) -> None:
        if self.__player is None or self.__match is None or not self.__cards:
            return

        # Desenha as cartas
        for icard in self.__cards:
            image = self.__flipped_card if not self.__match.ready else None
            icard.draw(surface, image)
