import pygame

NEIGHBOR_OFFSETS = [
    (0, 0),
    (0, 1),
    (0, -1),
    (1, 0),
    (1, 1),
    (1, -1),
    (-1, -1),
    (-1, 1),
    (-1, 0),
]

PHYSICS_TILES = {'tiles', 'items'}

MAP_LENGTH_IN_TILES = 10_000


class Tilemap:
    def __init__(self, game_or_editor, tilemap_data={}, tile_size=64):
        self.tile_size = tile_size
        self.offgrid_tiles = []
        self.game = game_or_editor
        self.tilemap = tilemap_data

    def tiles_around(self, compare_position):
        tiles = []
        tile_position = (int(compare_position[0] // self.tile_size), int(
            # pixel position to grid position
            compare_position[1] // self.tile_size))
        for offset in NEIGHBOR_OFFSETS:
            check_position = str(
                tile_position[0] + offset[0]) + ';' + str(tile_position[1] + offset[1])
            if check_position in self.tilemap:
                tiles.append(self.tilemap[check_position])

        return tiles

    def physics_rects_around(self, position) -> list[pygame.Rect]:
        rects = []
        for tile in self.tiles_around(position):
            if tile['type'] in PHYSICS_TILES:
                rects.append(pygame.Rect(tile['position'][0] * self.tile_size,
                             tile['position'][1] * self.tile_size, self.tile_size, self.tile_size))
        return rects
    
    def render(self, surface: pygame.Surface, camera_offset=(0, 0)):
        # for tile in self.offgrid_tiles:
        #     pass

        font = pygame.font.SysFont(None, 24)
        int_offset = (int(camera_offset[0]), int(camera_offset[1]))

        for x in range(int_offset[0] // self.tile_size, (int_offset[0] + surface.get_width()) // self.tile_size + 1):
            for y in range(int_offset[1] // self.tile_size, (int_offset[1] + surface.get_height()) // self.tile_size + 1):
                key = str(x) + ';' + str(y)
                if key in self.tilemap:
                    tile = self.tilemap[key]

                    position = (tile['position'][0] * self.tile_size - int_offset[0],
                                tile['position'][1] * self.tile_size - int_offset[1])

                    rect = pygame.Rect(
                        position[0], position[1], self.tile_size, self.tile_size)

                    pygame.draw.rect(surface, (50, 50, 50), rect)
                    pygame.draw.rect(surface, (15, 15, 15), rect, 1)

                    text_surface = font.render(
                        f"{tile['position']}", True, (255, 255, 255))
                    surface.blit(text_surface, position)
