import abc
import pygame
import threading

from assets.components import Component, WarningText


def on_event(type_: int):
    """Decorator for event callbacks.

    Args:
        type_ (int): The type of the event.
    """

    def inner(func: callable):
        Engine.add_event(type_, func)
        return func
    return inner


class Engine(metaclass=abc.ABCMeta):
    _width: int
    _height: int
    _fps: int

    _surface: pygame.Surface
    _clock: pygame.time.Clock

    __is_running: bool

    __server_thread: threading.Thread
    __components: dict[str, Component]

    __instances: int = 0
    __events: dict[int, list[callable]] = {}

    def __new__(cls, *args, **kwargs):
        cls.__instances += 1
        if cls.__instances > 1:
            raise RuntimeError("Only one instance of Engine can be created")
        return super().__new__(cls)

    def __init__(self, width: int = 800, height: int = 600, fps: int = 60, caption: str = "Window") -> None:
        """Initializes the game engine.

        Args:
            width (int, optional): The width of the game window. Defaults to 800.
            height (int, optional): The height of the game window. Defaults to 600.
            fps (int, optional): The target FPS of the game. Defaults to 60.
            caption (str, optional): The window caption. Defaults to "Window".
        """

        self._width, self._height = width, height
        self._fps = fps

        pygame.init()

        if not pygame.font.get_init():  # A fonte já e inicializada no comando acima, mas caso não seja, inicializa
            pygame.font.init()

        pygame.display.set_caption(caption)
        self._surface = pygame.display.set_mode((self._width, self._height))
        self._clock = pygame.time.Clock()

        self.__is_running = True
        self.__components = {}

        # O servidor precisa estar em uma thread separada, para não bloquear a thread principal
        self.__server_thread = threading.Thread(target=self.__handle_server)

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @staticmethod
    def add_event(type_: int, callback: callable) -> None:
        """Adiciona um callback de eventos.

        Args:
            type_ (int): O tipo do evento.
            callback (callable): O callback.
        """

        if type_ not in Engine.__events.keys():
            Engine.__events[type_] = []

        Engine.__events[type_].append(callback)

    def __handle_events(self) -> None:
        """Lida com eventos."""

        for event in pygame.event.get():
            # Usuario fechou a janela
            if event.type == pygame.QUIT:
                self.__is_running = False

            if event.type == pygame.KEYDOWN:
                try:
                    for comp in self.__components.values():  # Desenha os componentes
                        comp.on_keydown(event)
                except RuntimeError:
                    pass

            if event.type in self.__events.keys():
                for callback in self.__events[event.type]:
                    callback(self, event)

    def __handle_server(self) -> None:
        """Lida com o servidor."""

        ups = 20  # Limita o servidor a 20 tps

        last = pygame.time.get_ticks()
        while self.__is_running:
            if pygame.time.get_ticks() - last >= 1000 // ups:
                self.update_server()
                last = pygame.time.get_ticks()

    def add_component(self, component: Component, id: str = None) -> None:
        """Adiciona um componente à tela

        Args:
            id (str, optional): O id do componente. None por padrão
            component (Component): O componente a ser adicionado.
        """

        self.__components[id or str(len(self.__components))] = component

    def get_component(self, id: str) -> Component | None:
        """Pega um componente da tela.

        Args:
            id (str): id do componente.

        Returns:
            Component | None: O componente, se encontrado
        """

        return self.__components.get(id, None)

    def clear_components(self) -> None:
        """Remove todos os componentes da tela."""

        # Filtrar para que apenas warnings não sejam removidos
        temp = self.__components.copy()
        self.__components.clear()
        for key, comp in temp.items():
            if isinstance(comp, WarningText):
                self.__components[key] = comp

    def pop_component(self, id: str | None) -> Component | None:
        """Remove um componente da tela.

        Args:
            id (str): id do componente.
        """

        return self.__components.pop(id, None)

    def run(self) -> None:
        """Roda o jogo."""

        dt = 0
        self.init()  # Inicializa o jogo
        self.__server_thread.start()  # Inicia a thread do servidor
        while self.__is_running:
            self.__handle_events()  # Lida com eventos

            self.update(dt)  # Atualiza o jogo
            try:
                for key, comp in self.__components.items():  # Atualiza os componentes
                    comp.update(dt)
                    if isinstance(comp, WarningText) and comp.is_expired:
                        self.pop_component(key)  # Remove o componente caso tenha expirado
            except RuntimeError:
                pass

            self.draw()  # Desenha o jogo
            try:
                for comp in self.__components.values():  # Desenha os componentes
                    comp.draw(self._surface)
            except RuntimeError:
                pass

            pygame.display.flip()  # Atualiza a tela
            dt = self._clock.tick(self._fps) / 1000  # Atualiza o delta time

    @abc.abstractmethod
    def init(self) -> None:
        """Inicializa o jogo."""
        pass

    @abc.abstractmethod
    def update(self, dt: float) -> None:
        """Atualiza o jogo."""
        pass

    @abc.abstractmethod
    def update_server(self) -> None:
        """Atualiza o servidor."""
        pass

    @abc.abstractmethod
    def draw(self) -> None:
        """Desenha o jogo."""
        pass
