import json
import os
import pygame

from scripts.constants import TILE_SIZE
from scripts.tilemap import Tilemap

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
    return Tilemap(game_or_editor, data)

def screen_to_tilemap_position(screen_position, camera_offset) -> tuple[int, int]:
    x = (screen_position[0] + camera_offset[0]) // TILE_SIZE
    y = (screen_position[1] + camera_offset[1]) // TILE_SIZE
    return (x, y)

def save_tilemap_to_json(editor_tilemap, filename):
    try:
        with open(filename, 'w') as file:
            json.dump(editor_tilemap.to_json(), file, indent=4)
        print("Saved tilemap to", filename)
    except Exception as e:
        print(f"Failed to save tilemap to {filename}: {e}")

def load_tilemap_data_from_json(filename):
    try:
        with open(filename, 'r') as file:
            tilemap = json.load(file)
        print("Loaded tilemap from", filename)
        return tilemap
    except Exception as e:
        print(f"Failed to load tilemap from {filename}: {e}")
        return {}