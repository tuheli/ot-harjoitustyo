import pygame

from scripts.constants import SCREEN_HEIGHT, SCREEN_WIDTH
from scripts.editor.editor import Editor


class EditorApp:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption('The Impossible Game - Editor')
        screen_size = (SCREEN_WIDTH, SCREEN_HEIGHT)
        self.screen = pygame.display.set_mode(screen_size)
        self.editor = Editor(self.screen, self.stop)
        self.is_running = True

    def stop(self):
        self.is_running = False

    def run(self):
        while self.is_running:
            self.editor.run()


if __name__ == '__main__':
    EditorApp().run()
