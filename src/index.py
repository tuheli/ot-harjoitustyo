import sys
import pygame

from scripts import utils
from scripts.entities import PhysicsEntity
from scripts.tilemap import Tilemap


class Game:
  def __init__(self):
    pygame.init()
    pygame.display.set_caption('The Impossible Game')
    screen_size = (640 * 2, 480 * 2)
    self.screen = pygame.display.set_mode(screen_size)
    self.clock = pygame.time.Clock()

    self.movement = [False, False]

    self.assets = {
      'player': utils.load_image('/characters/platformChar_idle.png'),
      'tiles': utils.load_images('/tiles'),
      'items': utils.load_images('/items'),
    }

    self.player = PhysicsEntity(self, 'player', (6 * 64, 0), (64, 64))
    self.tilemap = Tilemap(self, tile_size=64)
    self.camera_offset = [0, 0]
    self.camera_offset_speed = 8 # same as player speed

  def run(self):
    while True:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_UP:
            self.player.velocity[1] = -20

      self.movement[1] = True

      self.screen.fill((14, 219, 248))

      self.player.update(tilemap=self.tilemap, movement=(self.movement[1] - self.movement[0], 0))

      self.camera_offset[0] += self.camera_offset_speed
      self.tilemap.render(self.screen, camera_offset=self.camera_offset)

      # physics_tiles_around = self.tilemap.physics_rects_around(self.player.position)
      # for rect in physics_tiles_around:
      #   pygame.draw.rect(self.screen, (0, 220, 33), rect)
        
      # self.player.render_center_point(self.screen)
      self.player.render(self.screen, camera_offset=self.camera_offset)

      pygame.display.update()
      self.clock.tick(60)


Game().run()