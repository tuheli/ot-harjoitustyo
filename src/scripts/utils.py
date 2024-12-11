import json
import os
import pygame

from scripts.constants import TILE_SIZE
from scripts.tilemap.tilemap import Tilemap

dirname = os.path.join(os.path.dirname(__file__))
base_image_path = os.path.join(dirname, '../../assets/images')


def load_image(path: str):
    img = pygame.image.load(base_image_path + path).convert()
    img.set_colorkey((0, 0, 0))
    return img


def load_images(path: str):
    images = []
    for img_name in sorted(os.listdir(base_image_path + path)):
        images.append(load_image(path + '/' + img_name))
    return images


def get_tilemap(game_or_editor) -> Tilemap:
    data = load_tilemap_data_from_json('tilemap.json')
    tilemap = data["tilemap"]
    player_start = data["player_start"]
    return Tilemap(game_or_editor, tilemap_data=tilemap, player_start=player_start)


def screen_to_tilemap_position(screen_position, camera_offset) -> tuple[int, int]:
    x = (screen_position[0] + camera_offset[0]) // TILE_SIZE
    y = (screen_position[1] + camera_offset[1]) // TILE_SIZE
    return (x, y)


def tilemap_to_screen_position(tilemap_position, camera_offset) -> tuple[int, int]:
    x = tilemap_position[0] * TILE_SIZE - camera_offset[0]
    y = tilemap_position[1] * TILE_SIZE - camera_offset[1]
    return (x, y)


def save_tilemap_to_json(editor_tilemap, filename):
    try:
        with open(filename, 'w') as file:
            json.dump(editor_tilemap.to_json(), file, indent=4)
        print("Saved tilemap to", filename)
    except Exception as e:
        print(f"Failed to save tilemap to {filename}: {e}")


def load_tilemap_data_from_json(filename):
    """
    Loads tilemap data from a JSON file.
    Return value is dict like: {
        'tilemap: {
            '0;0': {
                'type': 'tiles',
                'variant': 0,
                'position': (0, 0)
            },
            '2;4': {
                'type': 'tiles',
                'variant': 0,
                'position': (2, 4)
            },
        },
        'player_start': (0, 0)
    }
    """
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
        if "tilemap" not in data:
            data["tilemap"] = {}
        if "player_start" not in data:
            data["player_start"] = (0, 0)
        print("Loaded tilemap from", filename)
        return data
    except Exception as e:
        print(f"Failed to load tilemap from {filename}: {e}")
        return {}
