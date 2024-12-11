import pygame

class Particle:
    def __init__(self, position, velocity, size, color, lifetime):
        self.position = list(position)
        self.velocity = list(velocity)
        self.size = size
        self.color = color
        self.lifetime = lifetime

    def update(self, delta_time):
        self.position[0] += self.velocity[0] * delta_time
        self.position[1] += self.velocity[1] * delta_time
        self.lifetime -= delta_time

    def render(self, surface, camera_offset):
        if self.lifetime > 0:
            screen_position = (self.position[0] - camera_offset[0], self.position[1] - camera_offset[1])
            rect = pygame.Rect(screen_position[0], screen_position[1], self.size, self.size)
            pygame.draw.rect(surface, self.color, rect)