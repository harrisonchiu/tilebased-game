import pygame, sys
from os import path

# Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGRAY = (40, 40, 40)
LIGHTGRAY = (100, 100, 100)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Game settings
WIDTH = 1280   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 720  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60
TITLE = "Tilemap Demo"
TILESIZE = 64
MAPWIDTH = 100
MAPHEIGHT = 100
vec = pygame.math.Vector2

dir1 = path.dirname(__file__)
imagesdir = path.join(path.dirname(__file__), 'Resource')


# Player settings
PLAYER_SPEED = 300
