import time
import pygame
from typing import Self
from core.graphics import Resources
from core.game.match import Match
from core.game.cards import Card
from util import lerp, Queue


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

    def draw(self, surface: pygame.Surface, image: pygame.Surface = None, disabled: bool = False) -> None:
        surface.blit(image or self.__card.image, (self.__x, self.__y))

        if disabled or image:
            rect = pygame.Surface((self.__card.image.get_width(), self.__card.image.get_height()), pygame.SRCALPHA)
            rect.fill((0, 0, 0, 128))
            surface.blit(rect, (self.__x, self.__y))

    def __is_hovering(self) -> bool:
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

        # Carrega a fonte
        self.__font = pygame.font.Font(f"./src/assets/fonts/ThaleahFat.ttf", 28)

        # Variavel para controlar o tempo entre os cliques
        self.__last_click = 0
        self.__holding_click = False

        # Fila de requisições para o servidor
        self.__requests = Queue[dict]()

    def __update_cards(self) -> None:
        if self.__player is None or self.__match is None:
            return

        hand = [card.name for card in self.__player.hand]
        interactive = [icard.card.name for icard in self.__cards]

        if hand != interactive:
            self.__cards.clear()

            if len(hand) == 0:
                return

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
        if not self.__match.ready:
            return
        
        for i, icard in enumerate(self.__cards):
            next_card = self.__cards[i + 1] if i + 1 < len(self.__cards) else None

            if icard.is_hovering(next_card):
                last = time.time() - self.__last_click
                playable = (
                    self.__match.is_playable(icard.card) and
                    self.__match.can_play(self.__player.id)
                ) if self.__match.ready else False
                if pygame.mouse.get_pressed()[0] and last > 0.3 and not self.__holding_click and playable:
                    self.__last_click = time.time()
                    self.__requests.push({"type": "PLAY", "index": i})
                
                icard.move(y=-30)
            else:
                icard.move(y=0)

    def update(self, match: Match, dt: float) -> None:
        self.__match = match
        self.__player = self.__match.get_player(self.__id)

        # Atualiza a lista de cartas
        self.__update_cards()
        self.__animate_cards()

        left_click = pygame.mouse.get_pressed()[0]
        if left_click:
            self.__holding_click = True
        elif not left_click and self.__holding_click:
            self.__holding_click = False

    def update_server(self, network) -> None:
        if self.__requests.is_empty():
            return

        request = self.__requests.pop()
        network.send(request)

    def draw(self, surface: pygame.Surface) -> None:
        if self.__player is None or self.__match is None:
            return

        # Desenha o nome do jogador
        if self.__player.name.lower() in ('italo', 'luige'):
            name = f'{self.__player.name} (Host)' if self.__player.id == 0 else f'{self.__player.name} (You)'
            color = 'cyan'
        else:
            name = f'{self.__player.name} (You)'
            color = 'yellow' if self.__player.id == 0 else 'white'

        text = self.__font.render(name, True, color)
        rect = text.get_rect()
        rect.midbottom = (self.__client.width // 2, self.__client.height - self.__flipped_card.get_height() - 20)
        surface.blit(text, rect)

        # Desenha uma seta indicando o turno
        if self.__match.ready and self.__match.turn == self.__player.id:
            indicator_text = self.__font.render('Your Turn', True, 'green')
            indicator_rect = text.get_rect()
            indicator_rect.bottomleft = rect.midtop
            indicator_rect.x -= indicator_text.get_width() // 2

            surface.blit(indicator_text, indicator_rect)

        # Desenha as cartas
        for icard in self.__cards:
            image = self.__flipped_card if not self.__match.ready else None
            playable = (
                self.__match.is_playable(icard.card) and
                self.__match.can_play(self.__player.id)
            ) if self.__match.ready else False

            icard.draw(surface, image, not playable)

    def __iter__(self):
        return iter(self.__cards)
