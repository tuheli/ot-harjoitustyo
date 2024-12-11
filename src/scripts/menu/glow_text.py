import pygame


class GlowText:
    def __init__(self, text, font, color, glow_color, position, glow_offset=10, glow_intensity=8):
        self.text = text
        self.font = font
        self.color = color
        self.glow_color = glow_color
        self.position = position
        self.glow_offset = glow_offset
        self.glow_intensity = glow_intensity

        self.text_surface = self.font.render(self.text, True, self.color)
        self.text_rect = self.text_surface.get_rect(center=self.position)

    def render(self, screen):
        glow_surface = pygame.Surface((self.text_rect.width + 2 * self.glow_offset,
                                      self.text_rect.height + 2 * self.glow_offset), pygame.SRCALPHA)
        glow_surface.fill((0, 0, 0, 0))

        for offset in range(1, self.glow_intensity + 1):
            glow_text_surface = self.font.render(
                self.text, True, self.glow_color)
            glow_text_rect = glow_text_surface.get_rect(
                center=(glow_surface.get_width() / 2, glow_surface.get_height() / 2))
            glow_surface.blit(
                glow_text_surface, (glow_text_rect.x + offset, glow_text_rect.y + offset))

        screen.blit(glow_surface, (self.text_rect.x -
                    self.glow_offset, self.text_rect.y - self.glow_offset))

        screen.blit(self.text_surface, self.text_rect)
