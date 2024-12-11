import pygame

from scripts.constants import SCREEN_HEIGHT, SCREEN_WIDTH
from scripts.editor.editor import Editor


class App:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption('The Impossible Game - Editor')
        screen_size = (SCREEN_WIDTH, SCREEN_HEIGHT)
        self.screen = pygame.display.set_mode(screen_size)
        self.editor = Editor(self.screen)

    def run(self):
        while True:
            self.editor.run()


App().run()
