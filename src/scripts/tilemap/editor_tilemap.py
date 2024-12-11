from scripts.tilemap.tilemap import Tilemap

# TODO: no need for a superclass, just plain functions 
# would be nice passing the tilemap as argument and modifying it

class EditorTilemap(Tilemap):
    def __init__(self, game_or_editor, tilemap_data=..., player_start=..., tile_size=64):
        super().__init__(game_or_editor, tilemap_data, player_start, tile_size)

    def to_json(self):
        """
        Converts the tilemap to a JSON-compatible format.

        Returns:
            dict: A dictionary representing the tilemap in a JSON-compatible format.
        """
        return_dict = {}
        return_dict['tilemap'] = {}
        for [key, value] in self.tilemap.items():
            return_dict['tilemap'][key] = value
        return_dict['player_start'] = self.player_start
        return return_dict

    def add_tile(self, tilemap_position: tuple[int, int], tile_type='tiles', variant=0):
        """
        Adds a tile to the tilemap at the specified tilemap position.

        Args:
            position (tuple[int, int]): The position in the tilemap where the tile should be added.
            tile_type (str): The type of the tile to add.
            variant (int): The variant of the tile to add.

        Example:
            add_tile((10, 5))
        """
        x = tilemap_position[0]
        y = tilemap_position[1]

        self.tilemap[str(x) + ';' + str(y)] = {
            'type': tile_type,
            'variant': variant,
            'position': (x, y)
        }

    def remove_tile(self, tilemap_position: tuple[int, int]):
        """
        Removes a tile from the tilemap at the specified tilemap position.

        Args:
            position (tuple[int, int]): The position in the tilemap where the tile should be removed.

        Example:
            remove_tile((10, 5))
        """
        x = tilemap_position[0]
        y = tilemap_position[1]

        if str(x) + ';' + str(y) in self.tilemap:
            del self.tilemap[str(x) + ';' + str(y)]

    def move_tiles(self, dx: int, dy: int):
        """
        Moves all tiles in the tilemap by the specified offsets.

        Args:
            dx (int): The offset to move tiles along the x-axis.
            dy (int): The offset to move tiles along the y-axis.

        Example:
            move_tiles(1, 0)  # Move tiles to the right by 1 tile
        """
        new_tilemap = {}
        for key, tile in self.tilemap.items():
            new_x = tile['position'][0] + dx
            new_y = tile['position'][1] + dy
            new_key = str(new_x) + ';' + str(new_y)
            new_tilemap[new_key] = {
                'type': tile['type'],
                'variant': tile['variant'],
                'position': (new_x, new_y)
            }
        self.tilemap = new_tilemap
