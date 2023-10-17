import pygame


def on_event(type_: int):
    """Decorator for event callbacks.

    Args:
        type_ (int): The type of the event.
    """

    def inner(func: callable):
        if type_ not in Engine.events.keys():
            Engine.events[type_] = []

        Engine.events[type_].append(func)
        return func
    return inner


class Engine:
    width: int
    height: int
    fps: int

    surface: pygame.Surface
    clock: pygame.time.Clock

    is_running: bool

    events: dict[int, list[callable]] = {}
    instances: int = 0

    def __new__(cls, *args, **kwargs):
        cls.instances += 1
        if cls.instances > 1:
            raise RuntimeError("Only one instance of Engine can be created")
        return super().__new__(cls)

    def __init__(self, width: int = 800, height: int = 600, fps: int = 60) -> None:
        """Initializes the game engine.

        Args:
            width (int, optional): The width of the game window. Defaults to 800.
            height (int, optional): The height of the game window. Defaults to 600.
            fps (int, optional): The target FPS of the game. Defaults to 60.
        """

        self.width, self.height = width, height
        self.fps = fps

        pygame.init()
        self.surface = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()

        self.is_running = True

    def __handle_events(self) -> None:
        """Handles events."""

        for event in pygame.event.get():
            # User closed the window
            if event.type == pygame.QUIT:
                self.is_running = False

            if event.type in self.events.keys():
                for callback in self.events[event.type]:
                    callback(self, event)

    def run(self) -> None:
        """Runs the game loop."""

        dt = 0
        self.init()  # Initialize the game
        while self.is_running:
            self.__handle_events()  # Handle events
            self.update(dt)  # Update the game state
            self.draw()  # Draw the game

            pygame.display.flip()  # Update the display
            dt = self.clock.tick(self.fps) / 1000.0  # Get the time since last frame

    def init(self) -> None:
        """Initializes the game."""
        pass

    def update(self, dt: float) -> None:
        """Updates the game state."""
        pass

    def draw(self) -> None:
        """Draws the game."""
        pass
