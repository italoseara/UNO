import pygame
import threading

from assets.components import Component


def on_event(type_: int):
    """Decorator for event callbacks.

    Args:
        type_ (int): The type of the event.
    """

    def inner(func: callable):
        Engine.add_event(type_, func)
        return func
    return inner


class Engine:
    _width: int
    _height: int
    _fps: int

    _surface: pygame.Surface
    _clock: pygame.time.Clock

    __is_running: bool

    __server_thread: threading.Thread
    __components: list[Component]

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

        if not pygame.font.get_init():  # A fonte já e inicializada no comando acima, mas caso n seja, inicializa
            pygame.font.init()

        pygame.display.set_caption(caption)
        self._surface = pygame.display.set_mode((self._width, self._height))
        self._clock = pygame.time.Clock()

        self.__is_running = True
        self.__components = []

        # Server needs to be in a separate thread, so it doesn't block the main thread
        self.__server_thread = threading.Thread(target=self.__handle_server)

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @staticmethod
    def add_event(type_: int, callback: callable) -> None:
        """Adds an event callback.

        Args:
            type_ (int): The type of the event.
            callback (callable): The callback.
        """

        if type_ not in Engine.__events.keys():
            Engine.__events[type_] = []

        Engine.__events[type_].append(callback)

    def __handle_events(self) -> None:
        """Handles events."""

        for event in pygame.event.get():
            # User closed the window
            if event.type == pygame.QUIT:
                self.__is_running = False

            if event.type == pygame.KEYDOWN:
                try:
                    for comp in self.__components:  # Draw The components
                        comp.on_keydown(event)
                except RuntimeError:
                    pass

            if event.type in self.__events.keys():
                for callback in self.__events[event.type]:
                    callback(self, event)

    def __handle_server(self) -> None:
        """Handles the server."""

        while self.__is_running:
            self.update_server()

    def add_component(self, component: Component) -> None:
        """Adds a component to the screen.

        Args:
            component (Component): The component to add.
        """

        self.__components.append(component)

    def clear_components(self) -> None:
        """Clears all components from the screen."""

        self.__components.clear()


    def run(self) -> None:
        """Runs the game loop."""

        dt = 0
        self.init()  # Initialize the game
        self.__server_thread.start()  # Start the server thread
        while self.__is_running:
            self.__handle_events()  # Handle events

            self.update(dt)  # Update the game state
            try:
                for comp in self.__components:  # Update The components
                    comp.update(dt)
            except RuntimeError:
                pass

            self.draw()  # Draw the game
            try:
                for comp in self.__components:  # Draw The components
                    comp.draw(self._surface)
            except RuntimeError:
                pass

            pygame.display.flip()  # Update the display
            dt = self._clock.tick(self._fps) / 1000.0  # Get the time since last frame

    def init(self) -> None:
        """Initializes the game."""
        pass

    def update(self, dt: float) -> None:
        """Updates the game state."""
        pass

    def update_server(self) -> None:
        """Updates the server state."""
        pass

    def draw(self) -> None:
        """Draws the game."""
        pass
