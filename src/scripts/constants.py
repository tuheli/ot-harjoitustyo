SCREEN_WIDTH = 640 * 2
SCREEN_HEIGHT = 480 * 2
TILE_SIZE = 64
TICK_SPEED = 60
PLAYER_SPEED = 1.0667 * 7  # tile size to tick ratio * movement per second in tiles
DEFAULT_TILEMAP_PATH = 'tilemaps/tilemap.json'
PLAYER_START = (6 * TILE_SIZE, 13 * TILE_SIZE)
EDITOR_CAMERA_SPEED = 20
RESET_FLOOR_HEIGHT = 20 * TILE_SIZE
PLAYER_SPEED_SETTINGS_DEFAULT = {
    'speed': PLAYER_SPEED,
    'multiplier': 1,
    'max_fall_speed': 20,
    'fall_acceleration': 2,
    'jump_force': -20
}
PLAYER_SPEED_SETTINGS_HARDER = {
    'speed': PLAYER_SPEED,
    'multiplier': 1.25,
    'max_fall_speed': 20,
    'fall_acceleration': 2.85,
    'jump_force': -20
}
PLAYER_SPEED_SETTINGS = PLAYER_SPEED_SETTINGS_DEFAULT