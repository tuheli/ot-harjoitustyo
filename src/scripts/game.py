import sys
import pygame

from scripts.constants import PLAYER_SPEED, PLAYER_START, TICK_SPEED, TILE_SIZE
from scripts.player import Player
from scripts.tilemap import Tilemap

BACKGROUND_COLOR = (14, 219, 248)
COUNTDOWN_DURATION = 3 * TICK_SPEED # seconds
CAMERA_LERP_RATE = 0.5


class Game:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.clock = pygame.time.Clock()

        self.movement = [False, False]
        self.is_jump_pending = False

        self.player = Player(
            self, 'player', PLAYER_START, (TILE_SIZE, TILE_SIZE))
        self.tilemap = Tilemap(self, TILE_SIZE)  # initialize to something
        self.camera_offset = [0, 0]
        self.camera_offset_speed = PLAYER_SPEED
        self.jump_pending_duration = 150  # milliseconds
        self.jump_pending_end_time = 0
        self.countdown_timer = COUNTDOWN_DURATION

    def on_enter_game(self, tilemap: Tilemap):
        # reset / re-create necessary things
        player_position = (
            tilemap.player_start[0] * TILE_SIZE, tilemap.player_start[1] * TILE_SIZE)
        self.player = Player(
            self, 'player', player_position, (TILE_SIZE, TILE_SIZE))
        camera_x_offset_tiles = 6
        camera_y_offset_tiles = 8
        self.camera_offset = [player_position[0] -
                              camera_x_offset_tiles * TILE_SIZE, player_position[1] - camera_y_offset_tiles * TILE_SIZE]
        self.is_jump_pending = False
        self.tilemap = tilemap
        self.countdown_timer = COUNTDOWN_DURATION

    def process_countdown(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.player.render(self.screen, camera_offset=self.camera_offset)
        self.tilemap.render(self.screen, camera_offset=self.camera_offset)

        player_screen_x = self.player.position[0] - self.camera_offset[0]
        player_screen_y = self.player.position[1] - self.camera_offset[1]

        countdown_seconds = self.countdown_timer / TICK_SPEED

        font = pygame.font.SysFont(None, 48)
        countdown_text = font.render(f"Starting in {countdown_seconds:.1f} sec", True, (255, 255, 255))
        text_rect = countdown_text.get_rect(center=(player_screen_x + TILE_SIZE // 2, player_screen_y - 30))
        self.screen.blit(countdown_text, text_rect)

        pygame.display.update()
        self.clock.tick(TICK_SPEED)

        self.countdown_timer -= 1

    def run(self, toggle_menu, on_player_died):
        while True:
            did_toggle_menu = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.is_jump_pending = True
                        self.jump_pending_end_time = pygame.time.get_ticks() + self.jump_pending_duration
                    if event.key == pygame.K_ESCAPE:
                        toggle_menu()
                        did_toggle_menu = True

            if self.countdown_timer > 0:
                self.process_countdown()
                if did_toggle_menu:
                    break
                return

            self.movement[1] = True

            self.screen.fill(BACKGROUND_COLOR)

            self.player.update(tilemap=self.tilemap, movement=(
                self.movement[1] - self.movement[0], 0))

            # is dead check
            is_dead = self.player.is_dead_this_frame()
            if is_dead:
                on_player_died()

            if self.is_jump_pending:
                did_jump = self.player.jump()  # do this after update to know if grounded or not
                if did_jump:
                    self.is_jump_pending = False
                # leaves the jump input pending for a while
                elif pygame.time.get_ticks() > self.jump_pending_end_time:
                    self.is_jump_pending = False

            # camera x position
            self.camera_offset[0] += self.camera_offset_speed

            # camera y position
            screen_height = self.screen.get_height()
            player_screen_y = self.player.position[1] - self.camera_offset[1]
            upper_threshold = screen_height // 3
            lower_threshold = 2 * screen_height // 3

            if player_screen_y < upper_threshold:
                target_y = self.player.position[1] - upper_threshold
                self.camera_offset[1] += (target_y - self.camera_offset[1]) * CAMERA_LERP_RATE
            elif player_screen_y > lower_threshold:
                target_y = self.player.position[1] - lower_threshold
                self.camera_offset[1] += (target_y - self.camera_offset[1]) * CAMERA_LERP_RATE

            self.tilemap.render(self.screen, camera_offset=self.camera_offset)
            self.player.render(self.screen, camera_offset=self.camera_offset)

            pygame.display.update()
            self.clock.tick(TICK_SPEED)

            if did_toggle_menu:
                break
