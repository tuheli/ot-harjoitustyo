import os
import pygame

from scripts.constants import TILE_SIZE
from scripts.game import Game
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

def get_tilemap(game: Game, level_index: int) -> Tilemap:
    print('getting level', level_index)
    return Tilemap(game, tile_size=TILE_SIZE)