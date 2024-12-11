import pygame


class LevelButton:
    def __init__(self, text: str, level_index: int, position=(0, 0)):
        self.rect = pygame.Rect(position[0], position[1], 200, 80)
        self.font = pygame.font.SysFont('Corbel', 52)
        self.text = self.font.render(text, True, (245, 245, 245))
        self.text_rect = self.text.get_rect()
        self.text_rect.topleft = (position[0], position[1])
        self.level_index = level_index

    def render(self, screen: pygame.Surface, draw_color):
        pygame.draw.rect(screen, draw_color,
                         self.rect)
        screen.blit(self.text, self.text_rect)