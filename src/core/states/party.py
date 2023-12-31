import time
import pygame

from assets.components import WarningText, Button, Text
from core.game.interactivecards import InteractiveCards
from core.game.player import Player
from core.game.match import Match
from core.graphics import Resources
from core.connection import Network
from util import Queue

from .menu import Menu
from .state import State


class Party(State):
    __id: int
    __match: Match | None

    __cards: InteractiveCards | None

    # Salvando objetos do pygame para não precisar carregar toda hora
    __flipped_cards: dict[str, pygame.Surface]
    __color_picker: pygame.Surface
    __font: pygame.font.Font

    # Fila de requisições
    __requests: Queue[dict]

    # Variaveis logicas
    __holding_mouse: bool
    __last_click: float

    def __init__(self, client) -> None:
        super().__init__(client)
        self.__match = None
        self.__id = -1

        # Redimensionar e rotacionar as cartas
        card_width = int(Resources.CARD_BACK.get_width() * 3.5)
        card_height = int(Resources.CARD_BACK.get_height() * 3.5)
        size = (card_width, card_height)

        self.__flipped_cards = {
            "left": pygame.transform.rotate(pygame.transform.scale(Resources.CARD_BACK, size), -90).convert(),
            "right": pygame.transform.rotate(pygame.transform.scale(Resources.CARD_BACK, size), 90).convert(),
            "top": pygame.transform.rotate(pygame.transform.scale(Resources.CARD_BACK, size), 180).convert(),
            "regular": pygame.transform.scale(Resources.CARD_BACK, size).convert_alpha()
        }

        cp_size = int(Resources.COLOR_PICKER.get_width() * 4), int(Resources.COLOR_PICKER.get_height() * 4)
        self.__color_picker = pygame.transform.scale(Resources.COLOR_PICKER, cp_size).convert_alpha()
        self.__color_picker.set_alpha(200)

        self.__font = pygame.font.Font(f"./src/assets/fonts/ThaleahFat.ttf", 28)
        self.__cards = None

        self.__requests = Queue[dict]()

        self.__holding_mouse = False
        self.__last_click = 0

    def __start_party(self, *_) -> None:
        if self.__match.get_number_of_players() < 2:
            self._client.add_component(
                WarningText("You need at least 2 players", self._client.width // 2, 370,
                            font_size=30, align="center"), id="left")
            return

        self.__requests.push({"type": "START"})
        self._client.pop_component("start")

    def __exit_party(self, *_) -> None:
        self._client.disconnect()
        self._client.close_server()
        self._client.state = Menu(self._client)

        if not self._client.get_component("left"):
            self._client.add_component(
                WarningText("You left the party", self._client.width // 2, 550,
                            font_size=30, align="center"), id="left")

    def __update_deck(self, dt: float) -> None:
        if not self.__match.ready or not self.__match.can_play(self.__id) or not self.__match.can_draw(self.__id):
            return

        if self.__holding_mouse or time.time() - self.__last_click < 0.5:
            return

        card = self.__flipped_cards["regular"]
        hitbox = pygame.Rect(165, 175, card.get_width(), card.get_height())

        if hitbox.collidepoint(*pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            self.__requests.push({"type": "DRAW"})
            self.__last_click = time.time()

    def __update_color_picker(self, dt: float) -> None:
        player = self.__match.get_player(self.__id)
        if player is None or not player.selecting_color:
            return

        options = {
            "green": pygame.Rect(0, 0, 50, 60),
            "red": pygame.Rect(0, 0, 50, 60),
            "yellow": pygame.Rect(0, 0, 60, 50),
            "blue": pygame.Rect(0, 0, 60, 50)
        }

        options["green"].center = (self._client.width // 2, self._client.height // 2 - 60)
        options["red"].center = (self._client.width // 2, self._client.height // 2 + 50)
        options["yellow"].center = (self._client.width // 2 + 55, self._client.height // 2)
        options["blue"].center = (self._client.width // 2 - 55, self._client.height // 2)

        for color, rect in options.items():
            if rect.collidepoint(*pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] and \
                    time.time() - self.__last_click > 0.5:
                self.__requests.push({"type": "SELECT_COLOR", "color": color})
                self.__last_click = time.time()

    def __draw_hand(self, surface: pygame.Surface, player: Player, position: str) -> None:
        def get_vpos(hd: int, j: int) -> int:
            return y - hd // 2 + j * space

        def get_hpos(hd: int, j: int) -> int:
            return x - hd // 2 + j * space

        flipped_card = self.__flipped_cards[position]
        card_dimension = flipped_card.get_width()\
            if position == "top" else flipped_card.get_height()

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
            case _:
                return

        if player.hand:
            max_space = -30
            max_dimension = 600 if position == "top" else 400

            space = min(card_dimension + max_space, max_dimension // len(player.hand))
            hand_dimension = (len(player.hand) - 1) * space + card_dimension

            for i, card in enumerate(player.hand):
                match position:
                    case "top":
                        surface.blit(flipped_card, (get_hpos(hand_dimension, i), y))
                    case "left" | "right":
                        surface.blit(flipped_card, (x, get_vpos(hand_dimension, i)))
        else:
            hand_dimension = 0

        if player.name.lower() in ("italo", "luige"):
            name = f"{player.name} (Host)" if player.id == 0 else player.name
            color = "cyan"
        else:
            name = player.name
            color = "yellow" if player.id == 0 else "white"

        text = self.__font.render(name, True, color)
        rect = text.get_rect()

        match position:
            case "top":
                rect.midtop = (x, y + flipped_card.get_height() + 5)
            case "bottom":
                rect.midbottom = (x, y - 5)
            case "left" | "right":
                rect.midbottom = (x + flipped_card.get_width() // 2, y - hand_dimension // 2 - 5)

        surface.blit(text, rect)

        # Desenha uma seta indicando o turno
        if self.__match.ready and self.__match.turn == player.id and not self.__match.over:
            indicator_text = self.__font.render('Playing...', True, 'green')
            indicator_rect = text.get_rect()

            if position == "top":
                indicator_rect.topleft = rect.midbottom
            else:
                indicator_rect.bottomleft = rect.midtop

            indicator_rect.x -= indicator_text.get_width() // 2

            surface.blit(indicator_text, indicator_rect)

    def __draw_cards(self, surface: pygame.Surface) -> None:
        players_len = self.__match.get_number_of_players()

        offsets = {
            2: ["top"],
            3: ["left", "right"],
            4: ["left", "right", "top"]
        }

        positions = offsets.get(players_len, [])

        for position in positions:
            player_id = (self.__id + 1) % players_len if position == "left" or players_len == 2 else \
                (self.__id - 1) % players_len if position == "right" else \
                (self.__id + 2) % players_len if position == "top" else None

            if player_id is not None:
                player = self.__match.get_player(player_id)
                if player is not None:
                    self.__draw_hand(surface, player, position)

    def __draw_discard(self, surface: pygame.Surface) -> None:
        for dcard in self.__match.discard:
            image = pygame.transform.rotate(dcard.card.image, dcard.rotation)
            rect = image.get_rect()
            rect.center = (self._client.width // 2 + dcard.offset[0], 
                           self._client.height // 2 + dcard.offset[1])

            surface.blit(image, rect)

    def __draw_deck(self, surface: pygame.Surface) -> None:
        card_width = self.__flipped_cards["regular"].get_width()
        card_height = self.__flipped_cards["regular"].get_height()

        for i in range(3):
            surface.blit(self.__flipped_cards["regular"], (165 - 2*i, 175 - 2*i))

            if not self.__match.ready or not self.__match.can_play(self.__id) or not self.__match.can_draw(self.__id):
                rect = pygame.Surface((card_width, card_height))
                rect.set_alpha(128)
                rect.fill((0, 0, 0))
                surface.blit(rect, (165 - 2*i, 175 - 2*i))

        # Desenha o número de cartas no baralho
        text = self.__font.render(str(len(self.__match.deck)), True, "white")
        rect = text.get_rect()
        rect.center = (165 + card_width // 2, 175 + card_height // 2)
        surface.blit(text, rect)

    def __draw_color_picker(self, surface: pygame.Surface) -> None:
        player = self.__match.get_player(self.__id)
        if player is None or not player.selecting_color:
            return

        rect = self.__color_picker.get_rect()
        rect.center = (self._client.width // 2, self._client.height // 2)

        surface.blit(self.__color_picker, rect)

    def __draw_winner(self, surface: pygame.Surface):
        if not self.__match.over:
            self._client.pop_component("win-message")
            self._client.pop_component("restart")
            return

        # Draw black transparent rect
        rect = pygame.Surface((self._client.width, self._client.height))
        rect.set_alpha(128)
        rect.fill((0, 0, 0))
        surface.blit(rect, (0, 0))

        if not self._client.get_component("restart"):
            winner_id = self.__match.winner
            winner = self.__match.get_player(winner_id)

            self._client.add_component(
                Text("You win!" if self._client.network.id == winner_id else f"{winner.name} wins!",
                     self._client.width // 2, self._client.height // 2,
                     font_size=48, align="center", font_color="green"), id="win-message")

            if self._client.network.id == 0:
                self._client.add_component(
                    Button("Restart", self._client.width // 2, self._client.height // 2 + 50, font_size=48, align="center",
                           font_color="#FFD800", hover_color="#FFEE75", width=200, height=50,
                           animation="up", on_click=self.__restart_match), id="restart")

    def __restart_match(self, *_) -> None:
        self.__requests.push({"type": "RESTART"})
        self._client.clear_components()
        self.init()

    def init(self) -> None:
        self._client.add_component(
            Button("x", self._client.width - 20, 20, font_size=30, align="center",
                   width=30, height=30, animation=None, on_click=self.__exit_party))

        client_id = self._client.network.id

        if client_id == 0:
            self._client.add_component(
                Button("> Start", self._client.width // 2, self._client.height // 2, font_size=48, align="center",
                       font_color="#FFD800", hover_color="#FFEE75", width=200, height=50,
                       animation="up", on_click=self.__start_party), id="start")

        self.__cards = InteractiveCards(client_id, self._client)

    def update(self, dt: float) -> None:
        if self.__match is None:
            return

        if not self.__match.host_online:
            self.__exit_party()
            self._client.add_component(
                WarningText("Host left the party", self._client.width // 2, 550,
                            font_size=30, align="center"), id="left")

        self.__cards.update(self.__match, dt)
        self.__update_deck(dt)
        self.__update_color_picker(dt)

        if pygame.mouse.get_pressed()[0]:
            self.__holding_mouse = True
        elif self.__holding_mouse:
            self.__holding_mouse = False

    def update_server(self, network: Network) -> None:
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

        if not self.__requests.is_empty():
            request = self.__requests.pop()
            network.send(request)

        if self.__cards is not None:
            self.__cards.update_server(network)

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(Resources.BACKGROUND, (0, 0))

        if self.__match is None:
            return

        # Draw Cards
        self.__draw_cards(surface)
        self.__cards.draw(surface)

        self.__draw_deck(surface)
        self.__draw_discard(surface)
        self.__draw_color_picker(surface)

        self.__draw_winner(surface)
