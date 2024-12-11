import pygame


class Line:
    def __init__(self, start, end, color, width=4):
        self.start = start
        self.end = end
        self.color = color
        self.width = width

    def render(self, screen):
        pygame.draw.line(screen, self.color, self.start, self.end, self.width)
