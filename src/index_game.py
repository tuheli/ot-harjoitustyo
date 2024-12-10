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
        self.game.tilemap = get_tilemap(self)
        self.is_on_menu = True
        self.active_level = 0
        self.level_attempts = {
            0: 0,  # level index, attempt count
            1: 0,
            2: 0,
            3: 0,
        }

    def on_player_died(self):
        self.level_attempts[self.active_level] += 1
        print(
            f'attempt count for level {self.active_level} is {self.level_attempts.get(self.active_level)}')
        self.load_game(self.active_level)

    def load_game(self, selected_level):
        self.active_level = selected_level
        print("selected level", selected_level,
              "loading default tilemap from file")
        tilemap = get_tilemap(self)
        self.game.on_enter_game(tilemap)
        self.is_on_menu = False

    def load_menu(self):
        self.is_on_menu = True

    def run(self):
        while True:
            if self.is_on_menu:
                self.menu.run(self.load_game)
            else:
                self.game.run(self.load_menu, self.on_player_died)


App().run()
