import sys
import pygame

from scripts.constants import EDITOR_CAMERA_SPEED, TICK_SPEED, TILE_SIZE, DEFAULT_TILEMAP_PATH
from scripts.tilemap.editor_tilemap import EditorTilemap
from scripts.utils import save_tilemap_to_json, screen_to_tilemap_position, load_tilemap_data_from_json


class Editor:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.active_tilemap_path = DEFAULT_TILEMAP_PATH
        self.load_active_tilemap_from_file()

        self.movement = [False, False, False, False]

        player_position = (
            self.tilemap.player_start[0] * TILE_SIZE, self.tilemap.player_start[1] * TILE_SIZE)
        camera_x_offset_tiles = 6
        camera_y_offset_tiles = 8
        self.camera_offset = [player_position[0] -
                              camera_x_offset_tiles * TILE_SIZE, player_position[1] - camera_y_offset_tiles * TILE_SIZE]

        self.camera_offset_speed = EDITOR_CAMERA_SPEED

        self.is_selecting = False
        self.selection_start = None
        self.selection_end = None
        self.selected_tiles = []

    def paint_tile(self):
        screen_position = pygame.mouse.get_pos()
        tilemap_position = screen_to_tilemap_position(
            screen_position, self.camera_offset)
        self.tilemap.add_tile(tilemap_position)

    def erase_tile(self):
        screen_position = pygame.mouse.get_pos()
        tilemap_position = screen_to_tilemap_position(
            screen_position, self.camera_offset)
        self.tilemap.remove_tile(tilemap_position)

    def set_player_start(self):
        screen_position = pygame.mouse.get_pos()
        print(f"screen pos {screen_position}")
        tilemap_position = screen_to_tilemap_position(
            screen_position, self.camera_offset)
        print(f"tilemap pos {tilemap_position}")
        self.tilemap.player_start = tilemap_position

    def select_tiles(self):
        if self.selection_start and self.selection_end:
            start_pos = screen_to_tilemap_position(
                self.selection_start, self.camera_offset)
            end_pos = screen_to_tilemap_position(
                self.selection_end, self.camera_offset)
            self.selected_tiles = []

            for x in range(min(start_pos[0], end_pos[0]), max(start_pos[0], end_pos[0]) + 1):
                for y in range(min(start_pos[1], end_pos[1]), max(start_pos[1], end_pos[1]) + 1):
                    self.selected_tiles.append((x, y))

            print(f"Selected tiles: {self.selected_tiles}")

    def render_info(self):
        font = pygame.font.SysFont(None, 24)
        keybinds = [
            ("W/A/S/D", "Move camera"),
            ("Left Click (Hold)", "Paint tile"),
            ("Right Click (Hold)", "Erase tile"),
            ("Ctrl + S", "Save tilemap"),
            ("T", "Set player start at mouse position"),
            ("R", "Reload tilemap file without saving"),
            ("Arrow Keys", "Move All Tiles"),
        ]

        y_offset = 10
        padding = 10
        text_height = font.get_height()
        item_count = len(keybinds) + 1 # +1 for the active tilemap path
        total_height = item_count * (text_height + padding) + padding 

        background_rect = pygame.Rect(5, 5, 350, total_height)
        pygame.draw.rect(self.screen, (50, 50, 50), background_rect)

        # shows active tilemap path on top
        font = pygame.font.SysFont(None, 24)
        text_surface = font.render(f"Editing tilemap: {self.active_tilemap_path}", True, (255, 255, 255))
        text_rect = text_surface.get_rect(topleft=(10, y_offset))

        padding = 5
        background_rect = pygame.Rect(
            text_rect.left - padding,
            text_rect.top - padding,
            text_rect.width + 2 * padding,
            text_rect.height + 2 * padding
        )
        pygame.draw.rect(self.screen, (50, 50, 50), background_rect)

        self.screen.blit(text_surface, text_rect)
        
        y_offset += 40 # margin after active tilemap path

        # shows keybinds
        for key, description in keybinds:
            text_surface = font.render(
                f"{key}: {description}", True, (255, 255, 255))
            self.screen.blit(text_surface, (10, y_offset))
            y_offset += text_height + padding

    def load_active_tilemap_from_file(self):
        tilemap = load_tilemap_data_from_json(self.active_tilemap_path)
        self.tilemap = EditorTilemap(
            self, tilemap_data=tilemap['tilemap'], player_start=tilemap['player_start'])

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_LCTRL:
                        save_tilemap_to_json(self.tilemap, self.active_tilemap_path)
                    elif event.key == pygame.K_w:
                        self.movement[0] = True
                    elif event.key == pygame.K_a:
                        self.movement[1] = True
                    elif event.key == pygame.K_s:
                        self.movement[2] = True
                    elif event.key == pygame.K_d:
                        self.movement[3] = True
                    elif event.key == pygame.K_LEFT:
                        self.tilemap.move_tiles(-1, 0)
                    elif event.key == pygame.K_RIGHT:
                        self.tilemap.move_tiles(1, 0)
                    elif event.key == pygame.K_UP:
                        self.tilemap.move_tiles(0, -1)
                    elif event.key == pygame.K_DOWN:
                        self.tilemap.move_tiles(0, 1)
                    elif event.key == pygame.K_t:
                        self.set_player_start()
                    elif event.key == pygame.K_r:
                        self.load_active_tilemap_from_file()
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_w:
                        self.movement[0] = False
                    elif event.key == pygame.K_a:
                        self.movement[1] = False
                    elif event.key == pygame.K_s:
                        self.movement[2] = False
                    elif event.key == pygame.K_d:
                        self.movement[3] = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                            self.is_selecting = True
                            self.selection_start = pygame.mouse.get_pos()
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        if self.is_selecting:
                            self.is_selecting = False
                            self.selection_end = pygame.mouse.get_pos()

            if not self.is_selecting and pygame.mouse.get_pressed()[0]:
                self.paint_tile()

            if not self.is_selecting and pygame.mouse.get_pressed()[2]:
                self.erase_tile()

            # velocity is not normalized which is okay for the editor
            if self.movement[0]:
                self.camera_offset[1] -= self.camera_offset_speed
            if self.movement[1]:
                self.camera_offset[0] -= self.camera_offset_speed
            if self.movement[2]:
                self.camera_offset[1] += self.camera_offset_speed
            if self.movement[3]:
                self.camera_offset[0] += self.camera_offset_speed

            self.screen.fill((14, 219, 248))

            self.tilemap.render(self.screen, camera_offset=self.camera_offset, show_debug=True)

            player_start_rect = pygame.Rect(
                self.tilemap.player_start[0] * TILE_SIZE - self.camera_offset[0], self.tilemap.player_start[1] * TILE_SIZE - self.camera_offset[1], TILE_SIZE, TILE_SIZE)

            pygame.draw.rect(self.screen, (255, 165, 0), player_start_rect)

            if self.is_selecting and self.selection_start:
                current_pos = pygame.mouse.get_pos()
                selection_rect = pygame.Rect(
                    min(self.selection_start[0], current_pos[0]),
                    min(self.selection_start[1], current_pos[1]),
                    abs(self.selection_start[0] - current_pos[0]),
                    abs(self.selection_start[1] - current_pos[1])
                )
                pygame.draw.rect(self.screen, (255, 255, 0), selection_rect, 2)

            self.render_info()

            pygame.display.update()
            self.clock.tick(TICK_SPEED)
