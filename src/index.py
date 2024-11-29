import pygame

from scripts.constants import SCREEN_HEIGHT, SCREEN_WIDTH
from scripts.game import Game
from scripts.menu import Menu


class App:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption('The Impossible Game')
        screen_size = (SCREEN_WIDTH, SCREEN_HEIGHT)
        self.screen = pygame.display.set_mode(screen_size)
        self.menu = Menu(self.screen)
        self.game = Game(self.screen)
        self.is_on_menu = True

    def toggle_menu(self):
        self.is_on_menu = not self.is_on_menu

    def run(self):
        while True:
            if self.is_on_menu:
                self.menu.run(self.toggle_menu)
            else:
                self.game.run(self.toggle_menu)


App().run()