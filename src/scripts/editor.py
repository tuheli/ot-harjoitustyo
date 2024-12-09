import sys
import pygame

from scripts.constants import PLAYER_START, TILE_SIZE, TILEMAP_SAVE_PATH
from scripts.editor_tilemap import EditorTilemap
from scripts.utils import save_tilemap_to_json, screen_to_tilemap_position, load_tilemap_data_from_json


class Editor:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.clock = pygame.time.Clock()

        self.movement = [False, False, False, False]
        tilemap = load_tilemap_data_from_json(TILEMAP_SAVE_PATH)
        self.tilemap = EditorTilemap(self, tilemap, TILE_SIZE) # initialize to something
        self.camera_offset = [0, 0]
        self.camera_offset_speed = 20

        self.is_selecting = False
        self.selection_start = None
        self.selection_end = None
        self.selected_tiles = []

    def paint_tile(self):
        screen_position = pygame.mouse.get_pos()
        tilemap_position = screen_to_tilemap_position(screen_position, self.camera_offset)
        self.tilemap.add_tile(tilemap_position)

    def erase_tile(self):
        screen_position = pygame.mouse.get_pos()
        tilemap_position = screen_to_tilemap_position(screen_position, self.camera_offset)
        self.tilemap.remove_tile(tilemap_position)

    def select_tiles(self):
        if self.selection_start and self.selection_end:
            start_pos = screen_to_tilemap_position(self.selection_start, self.camera_offset)
            end_pos = screen_to_tilemap_position(self.selection_end, self.camera_offset)
            self.selected_tiles = []

            for x in range(min(start_pos[0], end_pos[0]), max(start_pos[0], end_pos[0]) + 1):
                for y in range(min(start_pos[1], end_pos[1]), max(start_pos[1], end_pos[1]) + 1):
                    self.selected_tiles.append((x, y))

            print(f"Selected tiles: {self.selected_tiles}")

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_LSHIFT:
                        save_tilemap_to_json(self.tilemap, TILEMAP_SAVE_PATH)
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

            if self.movement[0]:
                self.camera_offset[1] -= self.camera_offset_speed
            if self.movement[1]:
                self.camera_offset[0] -= self.camera_offset_speed
            if self.movement[2]:
                self.camera_offset[1] += self.camera_offset_speed
            if self.movement[3]:
                self.camera_offset[0] += self.camera_offset_speed

            self.screen.fill((14, 219, 248))

            self.tilemap.render(self.screen, camera_offset=self.camera_offset)

            player_start_rect = pygame.Rect(PLAYER_START[0] - self.camera_offset[0], PLAYER_START[1] - self.camera_offset[1], TILE_SIZE, TILE_SIZE)
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

            pygame.display.update()
            self.clock.tick(60)
