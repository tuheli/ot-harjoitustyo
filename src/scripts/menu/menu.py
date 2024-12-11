import pygame

from scripts.menu.glow_text import GlowText
from scripts.menu.glow_text_button import GlowTextButton

COLOR_LIGHT = (170, 170, 170)
COLOR_DARK = (100, 100, 100)
COLOR_BACKGROUND = (5, 5, 5)
COLOR_TEXT = (255, 255, 255)
COLOR_TEXT_GLOW = (0, 100, 255, 50)

class Menu:
    def __init__(self, screen: pygame.Surface, load_game_callback, set_active_tilemap_path_callback) -> None:
        self.screen: pygame.Surface = screen
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()

        self.load_game_callback = load_game_callback
        self.set_active_tilemap_path_callback = set_active_tilemap_path_callback

        title_text = "The Impossible Game"
        title_font = pygame.font.SysFont(None, 72)
        title_position = (self.width / 2, 100)
        self.title = GlowText(title_text, title_font, COLOR_TEXT, COLOR_TEXT_GLOW, title_position)

        self.button_size = (200, 80)
        self.level_buttons: list[GlowTextButton] = []

        button_y_gap = 100
        first_button_y = 300
        center_x = self.width / 2
        for i in range(4):
            position = (center_x, first_button_y)
            text = f'Level {i}'
            button = GlowTextButton(
                text, 
                title_font, 
                COLOR_TEXT, 
                COLOR_TEXT_GLOW, 
                position, 
                COLOR_DARK,
                COLOR_LIGHT,
                size=self.button_size,
                on_click=lambda: self.on_click_button(f'tilemap.json')
            )
            self.level_buttons.append(button)
            first_button_y += button_y_gap

    def on_click_button(self, tilemap_path):
        self.set_active_tilemap_path_callback(tilemap_path)
        self.load_game_callback()

    def run(self):
        while True:
            self.screen.fill(COLOR_BACKGROUND)
            mouse_position = pygame.mouse.get_pos()

            self.title.render(self.screen)

            active_level_button = None
            for button in self.level_buttons:
                is_active = False
                if button.button_rect.collidepoint(mouse_position):
                    is_active = True
                    active_level_button = button
                button.render(self.screen, is_active)

            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    if active_level_button is not None:
                        active_level_button.on_click()
                        return

            pygame.display.update()
