def main():
    try:
        import pygame
    except ImportError:
        print("ERROR: Pygame is not installed. Please install it using `pip install pygame`")
        exit(1)

    if pygame.version.vernum < (2, 5, 0):
        print("ERROR: Pygame version is too old. Please update it using `pip install pygame --upgrade`")
        exit(1)

    from game import Game
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
