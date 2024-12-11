import pygame

from scripts.constants import DEFAULT_TILEMAP_PATH
from scripts.menu.glow_text import GlowText
from scripts.menu.glow_text_button import GlowTextButton
from scripts.menu.line import Line

COLOR_LIGHT = (0, 156, 255) 
COLOR_DARK = (0, 94, 180)
COLOR_BACKGROUND = (5, 5, 5)
COLOR_TEXT = (255, 255, 255)
COLOR_TEXT_GLOW = (0, 100, 255, 50)
FIRST_LINE_COLOR = (5, 120, 240)


class Menu:
    def __init__(self, screen: pygame.Surface, load_game_callback, set_active_tilemap_path_callback) -> None:
        self.screen: pygame.Surface = screen
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()

        self.load_game_callback = load_game_callback
        self.set_active_tilemap_path_callback = set_active_tilemap_path_callback

        title_text = "The Impossible Game"
        title_font = pygame.font.SysFont(None, 100)
        title_position = (self.width / 2, 200)
        self.title = GlowText(title_text, title_font, COLOR_TEXT, COLOR_TEXT_GLOW, title_position)

        self.button_size = (400, 80)
        self.level_buttons: list[GlowTextButton] = []

        button_y_gap = 100
        first_button_y = 400
        center_x = self.width / 2
        button_font = pygame.font.SysFont(None, 62)
        for i in range(4):
            on_click = None
            text = ''
            if i == 0:
                on_click=lambda: self.on_click_button(DEFAULT_TILEMAP_PATH)
                text = f'Level {i + 1}'
            else:
                on_click=lambda: None
                text = f'Level {i + 1} (locked)'
            position = (center_x, first_button_y)
            button = GlowTextButton(
                text, 
                button_font, 
                COLOR_TEXT, 
                COLOR_TEXT_GLOW, 
                position, 
                background_color_normal=COLOR_DARK,
                background_color_active=COLOR_LIGHT,
                size=self.button_size,
                on_click=on_click,
                glow_intensity=0
            )
            self.level_buttons.append(button)
            first_button_y += button_y_gap

        line_x = 160
        self.left_side_lines = self.create_faded_lines('left', line_x)
        self.right_side_lines = self.create_faded_lines('right', screen.get_width() - line_x)

    def create_faded_lines(self, direction, start_x):
        lines: list[Line] = []
        line_color = FIRST_LINE_COLOR
        line_start_x = start_x
        line_position_offset = 10
        blue_fade_strength = 50
        green_fade_strength = 30
        for _ in range(4):
            start = (line_start_x, 300)
            end = (line_start_x, 800)
            line = Line(start, end, line_color)
            lines.append(line)
            if direction == 'right':
                line_start_x += line_position_offset
                line_color = (line_color[0], line_color[1] - green_fade_strength, line_color[2] - blue_fade_strength)
            else:
                line_start_x -= line_position_offset
                line_color = (line_color[0], line_color[1] - green_fade_strength, line_color[2] - blue_fade_strength)
        return lines


    def on_click_button(self, tilemap_path):
        self.set_active_tilemap_path_callback(tilemap_path)
        self.load_game_callback()

    def run(self):
        while True:
            self.screen.fill(COLOR_BACKGROUND)
            mouse_position = pygame.mouse.get_pos()

            self.title.render(self.screen)

            for line in self.left_side_lines:
                line.render(self.screen)

            for line in self.right_side_lines:
                line.render(self.screen)

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
