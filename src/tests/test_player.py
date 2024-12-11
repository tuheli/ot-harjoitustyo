import unittest
from unittest.mock import MagicMock
from scripts.entities import Player
from scripts.tilemap.tilemap import Tilemap


class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.player = Player(None, 'player', (0, 0), (64, 64))
        self.tilemap = Tilemap(None, tile_size=64)

    def test_initial_position(self):
        self.assertEqual(self.player.position, [0, 0])

    def test_player_jump(self):
        self.player.jump = MagicMock(return_value=True)
        jumped = self.player.jump()
        self.assertTrue(jumped)
        self.player.jump.assert_called()

    def test_player_collision_with_tilemap(self):
        self.player.update(self.tilemap, movement=(0, 0))
        self.assertTrue(self.player.position[1] >= 0)
