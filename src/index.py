import pygame

from scripts.constants import SCREEN_HEIGHT, SCREEN_WIDTH
from scripts.game import Game
from scripts.menu import Menu
from scripts.utils import get_tilemap


class App:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption('The Impossible Game')
        screen_size = (SCREEN_WIDTH, SCREEN_HEIGHT)
        self.screen = pygame.display.set_mode(screen_size)
        self.menu = Menu(self.screen)
        self.game = Game(self.screen)
        self.is_on_menu = True

    def load_game(self, selected_level):
        tilemap = get_tilemap(self.game, selected_level)
        self.game.on_enter_game(tilemap)
        self.is_on_menu = False

    def load_menu(self):
        self.is_on_menu = True

    def run(self):
        while True:
            if self.is_on_menu:
                self.menu.run(self.load_game)
            else:
                self.game.run(self.load_menu)


App().run()