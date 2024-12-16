import pygame

from scripts.constants import DEFAULT_TILEMAP_PATH, SCREEN_HEIGHT, SCREEN_WIDTH
from scripts.editor.editor import Editor
from scripts.game.game import Game
from scripts.game.app_state import AppState
from scripts.menu.menu import Menu
from scripts.utils import get_tilemap


class GameApp:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption('The Impossible Game')
        screen_size = (SCREEN_WIDTH, SCREEN_HEIGHT)
        self.screen = pygame.display.set_mode(screen_size)
        self.menu = Menu(self.screen, self.load_game,
                         self.set_active_tilemap_path, self.load_editor)
        self.game = Game(self.screen, self.load_menu, self.load_game)
        self.editor = Editor(self.screen, self.load_menu)
        self.active_tilemap_path = DEFAULT_TILEMAP_PATH
        self.game.tilemap = get_tilemap(self, self.active_tilemap_path)
        self.app_state = AppState.MENU

    def set_active_tilemap_path(self, tilemap_path):
        self.active_tilemap_path = tilemap_path

    def load_game(self):
        tilemap = get_tilemap(self, self.active_tilemap_path)
        self.game.reset(tilemap)
        self.app_state = AppState.GAMEPLAY

    def load_menu(self):
        self.app_state = AppState.MENU

    def load_editor(self):
        self.app_state = AppState.EDITOR

    def run(self):
        while True:
            if self.app_state == AppState.MENU:
                self.menu.run()
            elif self.app_state == AppState.EDITOR:
                self.editor.run()
            elif self.app_state == AppState.GAMEPLAY:
                self.game.run()
            else:
                raise ValueError(f'Invalid app state')

if __name__ == '__main__':
    GameApp().run()
