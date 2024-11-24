import pygame


class PhysicsEntity:
    def __init__(self, game, entity_type, position, size):
        self.game = game
        self.entity_type = entity_type
        self.position = list(position)
        self.size = size
        self.velocity = [0, 0]
        self.movespeed = 8
        self.max_fall_speed = 20
        self.fall_acceleration = 2
        self.collisions = {
            'top': False,
            'bottom': False,
            'left': False,
            'right': False
        }

    def rect(self) -> pygame.Rect:
        return pygame.Rect(self.position[0], self.position[1], self.size[0], self.size[1])

    def update(self, tilemap, movement=(0, 0)):
        self.collisions = {
            'top': False,
            'bottom': False,
            'left': False,
            'right': False
        }

        frame_movement = (movement[0] + self.velocity[0], self.velocity[1])

        self.position[0] += frame_movement[0] * self.movespeed
        
        # # horizontal collisions
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.position):
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0:
                    self.collisions['right'] = True
                    entity_rect.right = rect.left
                if frame_movement[0] < 0:
                    self.collisions['left'] = True
                    entity_rect.left = rect.right
                self.position[0] = entity_rect.x

        self.position[1] += frame_movement[1]

        # vertical collisions
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.position):
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:
                    self.collisions['bottom'] = True
                    entity_rect.bottom = rect.top
                if frame_movement[1] < 0:
                    self.collisions['top'] = True
                    entity_rect.top = rect.bottom
                self.position[1] = entity_rect.y

        self.velocity[1] = min(self.max_fall_speed, self.velocity[1] + self.fall_acceleration)

        if self.collisions['bottom'] or self.collisions['top']:
            self.velocity[1] = 0

    def render_center_point(self, surface: pygame.Surface):
        pygame.draw.circle(surface, (255, 0, 0), self.position, 3)
    
    def render(self, surface: pygame.Surface):
        image = self.game.assets[self.entity_type]
        scaled_image = pygame.transform.scale(image, (self.size[0], self.size[1]))
        surface.blit(scaled_image, self.position)