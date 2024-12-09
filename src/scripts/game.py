import sys
import pygame

from scripts.constants import PLAYER_START, TILE_SIZE
from scripts.entities import Player
from scripts.tilemap import Tilemap


class Game:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.clock = pygame.time.Clock()

        self.movement = [False, False]
        self.is_jump_pending = False

        self.player = Player(
            self, 'player', PLAYER_START, (TILE_SIZE, TILE_SIZE))
        self.tilemap = Tilemap(self, TILE_SIZE) # initialize to something
        self.camera_offset = [0, 0]
        self.camera_offset_speed = 8  # same as player speed
        self.jump_pending_duration = 150  # milliseconds
        self.jump_pending_end_time = 0

    def on_enter_game(self, tilemap: Tilemap):
        # reset / re-create necessary things
        self.player = Player(
            self, 'player', PLAYER_START, (TILE_SIZE, TILE_SIZE))
        self.camera_offset = [0, 0]
        self.is_jump_pending = False
        self.tilemap = tilemap

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

            self.movement[1] = True

            self.screen.fill((14, 219, 248))

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
            self.clock.tick(60)

            if did_toggle_menu:
                break
