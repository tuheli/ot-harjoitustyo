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

class Tilemap:
    def __init__(self, game, tile_size=64):
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgrid_tiles = []
        self.game = game

        for y in range(1):
            for x in range(20):
                x_pos = x
                y_pos = 10
                self.tilemap[str(x_pos) + f';{y_pos}'] = {
                    'type': 'tiles',
                    'variant': 4, # the file order index
                    'position': (x_pos, y_pos)
                }

        for x in range(1):
            for y in range(9, 10):
                x_pos = 4
                y_pos = y
                self.tilemap[str(x_pos) + f';{y_pos}'] = {
                    'type': 'tiles',
                    'variant': 4, # the file order index
                    'position': (x_pos, y_pos)
                }

        for x in range(1):
            for y in range(8, 10):
                x_pos = 7
                y_pos = y
                self.tilemap[str(x_pos) + f';{y_pos}'] = {
                    'type': 'tiles',
                    'variant': 4, # the file order index
                    'position': (x_pos, y_pos)
                }

    def rect(self, tile) -> pygame.Rect:
        grid_position = tile['position']
        return pygame.Rect(grid_position[0] * self.tile_size, grid_position[1] * self.tile_size, self.tile_size, self.tile_size)

    def tiles_around(self, compare_position):
        tiles = []
        tile_position = (int(compare_position[0] // self.tile_size), int(compare_position[1] // self.tile_size)) # pixel position to grid position
        for offset in NEIGHBOR_OFFSETS:
            check_position = str(tile_position[0] + offset[0]) + ';' + str(tile_position[1] + offset[1])
            if check_position in self.tilemap:
                tiles.append(self.tilemap[check_position])

        return tiles
    
    def physics_rects_around(self, position) -> list[pygame.Rect]:
        rects = []
        for tile in self.tiles_around(position):
            if tile['type'] in PHYSICS_TILES:
                rects.append(pygame.Rect(tile['position'][0] * self.tile_size, tile['position'][1] * self.tile_size, self.tile_size, self.tile_size))
        return rects
    
    def render(self, surface: pygame.Surface):
        for tile in self.offgrid_tiles:
            pass

        font = pygame.font.SysFont(None, 24)

        for key in self.tilemap:
            tile = self.tilemap[key]
            
            position = (tile['position'][0] * self.tile_size, tile['position'][1] * self.tile_size)
            
            pygame.draw.rect(surface, (50, 50, 50), self.rect(tile))
            pygame.draw.rect(surface, (15, 15, 15), self.rect(tile), 1)


            text_surface = font.render(f"{tile['position']}", True, (255, 255, 255))
            surface.blit(text_surface, position)
