import sys
import pygame

from scripts.constants import PLAYER_SPEED, PLAYER_START, TICK_SPEED, TILE_SIZE
from scripts.player import Player
from scripts.tilemap import Tilemap

BACKGROUND_COLOR = (14, 219, 248)
COUNTDOWN_DURATION = 1 # seconds


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
        self.countdown_timer = COUNTDOWN_DURATION * TICK_SPEED

    def on_enter_game(self, tilemap: Tilemap):
        # reset / re-create necessary things
        player_position = (
            tilemap.player_start[0] * TILE_SIZE, tilemap.player_start[1] * TILE_SIZE)
        self.player = Player(
            self, 'player', player_position, (TILE_SIZE, TILE_SIZE))
        camera_offset_tiles = 6
        self.camera_offset = [player_position[0] -
                              camera_offset_tiles * TILE_SIZE, 0]
        self.is_jump_pending = False
        self.tilemap = tilemap
        self.countdown_timer = COUNTDOWN_DURATION * TICK_SPEED

    def process_countdown(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.player.render(self.screen, camera_offset=self.camera_offset)
        self.tilemap.render(self.screen, camera_offset=self.camera_offset)

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

            self.camera_offset[0] += self.camera_offset_speed

            self.tilemap.render(self.screen, camera_offset=self.camera_offset)
            self.player.render(self.screen, camera_offset=self.camera_offset)

            pygame.display.update()
            self.clock.tick(TICK_SPEED)

            if did_toggle_menu:
                break
