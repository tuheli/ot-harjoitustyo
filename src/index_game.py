import pygame

from scripts.constants import SCREEN_HEIGHT, SCREEN_WIDTH
from scripts.game.game import Game
from scripts.menu.menu import Menu
from scripts.utils import get_tilemap

DEFAULT_TILEMAP_PATH = 'tilemap.json'


class App:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption('The Impossible Game')
        screen_size = (SCREEN_WIDTH, SCREEN_HEIGHT)
        self.screen = pygame.display.set_mode(screen_size)
        self.menu = Menu(self.screen, self.load_game, self.set_active_tilemap_path)
        self.game = Game(self.screen, self.load_menu, self.load_game)
        self.active_tilemap_path = DEFAULT_TILEMAP_PATH
        self.game.tilemap = get_tilemap(self, self.active_tilemap_path)
        self.is_on_menu = True

    def set_active_tilemap_path(self, tilemap_path):
        print("selected tilemap path", tilemap_path)
        self.active_tilemap_path = tilemap_path

    def load_game(self):
        print('loading game')
        tilemap = get_tilemap(self, self.active_tilemap_path)
        self.game.on_enter_game(tilemap)
        self.is_on_menu = False

    def load_menu(self):
        self.is_on_menu = True

    def run(self):
        while True:
            if self.is_on_menu:
                self.menu.run()
            else:
                self.game.run()


App().run()
