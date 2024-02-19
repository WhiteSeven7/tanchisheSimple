from pygame.math import Vector2
UP = Vector2(0, -1)
DOWN = Vector2(0, 1)
LEFT = Vector2(-1, 0)
RIGHT = Vector2(1, 0)

BODY_SIZE = 38
TILE_SIZE = 50
TILE_WIDTH = 16
TILE_HEIGHT = 12
SCORE_HEIGHT = 120
GAME_HEIGHT = TILE_HEIGHT * TILE_SIZE
SIZE = WIDTH, HEIGHT = TILE_WIDTH * TILE_SIZE, GAME_HEIGHT + SCORE_HEIGHT
APPLE_SIZE = 40

LIGHT_GREEN = '#79E344'
DARK_GREEN = '#294D17'