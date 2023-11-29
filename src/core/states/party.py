import pygame

from assets.components import Text, Button
from core.game.match import Match
from core.game.player import Player
from core.graphics import Resources
from core.connection import Network

from .menu import Menu
from .state import State


class Party(State):
    __match: Match | None
    __id: int

    # Imagens salvas para não ter que ficar redimensionando toda hora
    __flipped_cards: dict[str, pygame.Surface]

    def __init__(self, client):
        super().__init__(client)
        self.__match = None
        self.__id = -1

        # Redimensionar e rotacionar as cartas
        card_width = int(Resources.CARD_BACK.get_width() * 3.5)
        card_height = int(Resources.CARD_BACK.get_height() * 3.5)
        size = (card_width, card_height)

        self.__flipped_cards = {
            "left": pygame.transform.rotate(pygame.transform.scale(Resources.CARD_BACK, size), 90).convert(),
            "right": pygame.transform.rotate(pygame.transform.scale(Resources.CARD_BACK, size), -90).convert(),
            "top": pygame.transform.rotate(pygame.transform.scale(Resources.CARD_BACK, size), 180).convert(),
            "bottom": pygame.transform.scale(Resources.CARD_BACK, size).convert(),
        }

    def init(self):
        cx = self._client.width // 2
        cy = self._client.height // 2

        self._client.add_component(
            Text("Party", cx, cy, font_color="black", font_size=72, align="center"))

        self._client.add_component(
            Button("< Back", 10, 560, height=30, font_size=32, on_click=self.__exit_party))

    def __exit_party(self, *_):
        self._client.disconnect()
        self._client.close_server()
        self._client.state = Menu(self._client)

    def update(self, dt: float):
        pass

    def update_server(self, network: Network):
        if network is None:
            return

        # Se a partida já começou, volta para o menu de join
        self.__id = network.id
        if self.__id == -1:
            self.__exit_party()
            return

        match = network.send({"type": "GET"})
        if match is not None:
            self.__match = match

    def __draw_hand(self, surface: pygame.Surface, player: Player, position: str):
        def get_vpos(hd: int, j: int) -> int:
            return y - hd // 2 + j * space

        def get_hpos(hd: int, j: int) -> int:
            return x - hd // 2 + j * space

        flipped_card = self.__flipped_cards[position]
        card_dimension = flipped_card.get_width()\
            if position in ("top", "bottom")\
            else flipped_card.get_height()

        # Define a posição das cartas na tela
        match position:
            case "left":
                x = 20
                y = self._client.height // 2
            case "right":
                x = self._client.width - 20 - flipped_card.get_width()
                y = self._client.height // 2
            case "top":
                x = self._client.width // 2
                y = 20
            case "bottom":  # Propria mão
                x = self._client.width // 2
                y = self._client.height - 20 - flipped_card.get_height()
            case _:
                return

        max_space = -30
        max_dimension = 600 if position in ("top", "bottom") else 400

        space = min(card_dimension + max_space, max_dimension // len(player.hand))
        hand_dimension = (len(player.hand) - 1) * space + card_dimension

        for i, card in enumerate(player.hand):
            if position == "top":
                surface.blit(flipped_card, (get_hpos(hand_dimension, i), y))
            elif position == "bottom":
                # Desenha a carta virada para cima apenas se a partida já começou
                card_image = card.image if self.__match.ready else flipped_card
                surface.blit(card_image, (get_hpos(hand_dimension, i), y))
            else:
                surface.blit(flipped_card, (x, get_vpos(hand_dimension, i)))

    def __draw_cards(self, surface: pygame.Surface):
        players_len = self.__match.get_number_of_players()

        offsets = {
            2: ["top"],
            3: ["left", "right"],
            4: ["left", "right", "top"]
        }

        positions = offsets.get(players_len, [])

        for position in positions:
            player_id = (self.__id + 1) % players_len if position == "left" else \
                (self.__id - 1) % players_len if position == "right" else \
                (self.__id + 2) % players_len if position == "top" else None

            if player_id is not None:
                player = self.__match.get_player(player_id)
                if player is not None and player.hand:
                    self.__draw_hand(surface, player, position)

        player = self.__match.get_player(self.__id)
        if player.hand:
            # TODO: Tornar as cartas interativas
            self.__draw_hand(surface, player, "bottom")

    def draw(self, surface: pygame.Surface):
        surface.blit(Resources.BACKGROUND, (0, 0))

        if self.__match is None:
            return

        self.__draw_cards(surface)
