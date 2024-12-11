import pygame

from scripts.constants import DEFAULT_TILEMAP_PATH, SCREEN_HEIGHT, SCREEN_WIDTH
from scripts.editor.editor import Editor
from scripts.game.game import Game
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
        self.is_on_menu = True
        self.is_on_editor = False

    def set_active_tilemap_path(self, tilemap_path):
        print("selected tilemap path", tilemap_path)
        self.active_tilemap_path = tilemap_path

    def load_game(self):
        print('loading game')
        tilemap = get_tilemap(self, self.active_tilemap_path)
        # resets necessary things without recreating Game object
        self.game.reset(tilemap)
        self.is_on_menu = False
        self.is_on_editor = False

    def load_menu(self):
        self.is_on_menu = True
        self.is_on_editor = False

    def load_editor(self):
        self.is_on_editor = True
        self.is_on_menu = False

    def run(self):
        while True:
            if self.is_on_menu:
                self.menu.run()
            elif self.is_on_editor:
                self.editor.run()
            else:
                self.game.run()


if __name__ == '__main__':
    GameApp().run()
