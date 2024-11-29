import pygame

class LevelButton:
    def __init__(self, text: str, level_index: int, position = (0, 0)):
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

class Menu:
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen: pygame.Surface = screen
        self.color_text = (255,255,255)  
        self.color_light = (170,170,170)  
        self.color_dark = (100,100,100)  
        self.color_background = (5, 5, 5)
        self.width = self.screen.get_width()  
        self.height = self.screen.get_height()  

        self.button_size = (200, 80)
        self.level_buttons: list[LevelButton] = []

        button_y_gap = 100
        first_button_y = 300
        first_button_x = self.screen.get_height() / 2
        for i in range(4):
            position = (first_button_x, first_button_y)
            text = f'Level {i}'
            self.level_buttons.append(LevelButton(text, i, position))
            first_button_y += button_y_gap

    def run(self, on_click_level):
        while True:
            did_click_level = False

            self.screen.fill(self.color_background)

            mouse_position = pygame.mouse.get_pos()

            active_level_button = None
            for level_button in self.level_buttons:
                draw_color = self.color_dark
                if level_button.rect.collidepoint(mouse_position):
                    draw_color = self.color_light
                    active_level_button = level_button
                level_button.render(self.screen, draw_color)

            for ev in pygame.event.get():  
                if ev.type == pygame.QUIT:  
                    pygame.quit()
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    if active_level_button is not None:
                        on_click_level(active_level_button.level_index)
                        did_click_level = True

            pygame.display.update()  

            if did_click_level:
                break

  