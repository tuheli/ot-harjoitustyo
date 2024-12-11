from scripts.constants import PLAYER_SPEED_SETTINGS, RESET_FLOOR_HEIGHT
from scripts.entities.physics_entity import PhysicsEntity


class Player(PhysicsEntity):
    def __init__(self, game, entity_type, position, size):
        super().__init__(game, entity_type, position, size)
        self.is_dead = False
        multiplier = PLAYER_SPEED_SETTINGS['multiplier']
        self.movespeed = PLAYER_SPEED_SETTINGS['speed'] * multiplier
        self.max_fall_speed = PLAYER_SPEED_SETTINGS['max_fall_speed'] * multiplier
        self.fall_acceleration = PLAYER_SPEED_SETTINGS['fall_acceleration'] * multiplier
        self.jump_force = PLAYER_SPEED_SETTINGS['jump_force'] * multiplier

    def jump(self) -> bool:
        """
        Returns true if jump was a success.
        Has to be called after update.
        """
        if not self.collisions['bottom']:
            return False
        self.velocity[1] = self.jump_force
        return True

    def is_dead_this_frame(self):
        """
        Returns true if player died during this frame.
        Has to be called after update.
        """
        if self.collisions['right']:
            return True
        if self.collisions['top']:
            return True
        if self.position[1] >= RESET_FLOOR_HEIGHT:
            return True
        return False
