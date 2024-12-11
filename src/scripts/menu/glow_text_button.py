import pygame
from scripts.menu.glow_text import GlowText


class GlowTextButton(GlowText):
    def __init__(self, text, font, color, glow_color, position, background_color_normal, background_color_active, border_radius=10, glow_offset=10, glow_intensity=8, on_click=None, size=(200, 80)):
        super().__init__(text, font, color, glow_color, position, glow_offset, glow_intensity)
        self.background_color_active = background_color_active
        self.background_color_normal = background_color_normal
        self.border_radius = border_radius

        self.button_rect = self.text_rect.inflate(20, 20)
        self.button_rect = pygame.Rect(0, 0, *size)
        self.button_rect.center = position

        self.text_rect.center = self.button_rect.center

        self.on_click = on_click

    def render(self, screen, is_active):
        draw_color = self.background_color_normal
        if is_active:
            draw_color = self.background_color_active

        pygame.draw.rect(screen, draw_color, self.button_rect, border_radius=self.border_radius)

        super().render(screen)