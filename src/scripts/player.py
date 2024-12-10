from scripts.constants import PLAYER_SPEED, RESET_FLOOR_HEIGHT
from scripts.entities import PhysicsEntity


class Player(PhysicsEntity):
    def __init__(self, game, entity_type, position, size):
        super().__init__(game, entity_type, position, size)
        self.movespeed = PLAYER_SPEED

    def jump(self) -> bool:
        """
        Returns true if jump was a success.
        Has to be called after update.
        """
        if not self.collisions['bottom']:
            return False
        self.velocity[1] = -20
        return True

    def is_dead_this_frame(self):
        """
        Returns true if player died during this frame.
        Has to be called after update.
        """
        if self.collisions['right']:
            return True
        if self.position[1] >= RESET_FLOOR_HEIGHT:
            return True
        return False
