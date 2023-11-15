import sys
import pygame
from enum import Enum

# 60 FPS
FRAME_LENGTH: int = 1000 // 60

STARTING_LEVEL: int = 0
QUEUE_SIZE: int = 10

SCREEN_SIZE: (int,int) = (800, 800)
SCREEN_W, SCREEN_H = SCREEN_SIZE

"""
DIM variables are associated with the actual pixel sizes of the elements Do not
confuse these with non-DIM variables, which are associated with number of
blocks on the grid.
"""

# dimension size of a grid block
BLOCK_DIM: (int,int) = (35, 35)
BW, BH = BLOCK_DIM

# total size of grid
GRID_DIM: (int,int) = (10*BW, 20*BH)
GRID_DIM_W, GRID_DIM_H = GRID_DIM

# top left position of grid (centered)
# GRID_POS: (int,int) = ((SCREEN_W - GRID_DIM_W)/2, 0)
GRID_POS: (int,int) = ((SCREEN_W - GRID_DIM_W)/2, (SCREEN_H - GRID_DIM_H)/2) # with horizontal centered
GX, GY = GRID_POS

GRID_BLOCK_COUNT: (int,int) = (10, 25)
GRID_BLOCK_OFFSET_Y: int = 5
GW, GH = GRID_BLOCK_COUNT
GHO: int = GH-GRID_BLOCK_OFFSET_Y # grid height with offset

INT_MAX: int = sys.maxsize
INT_MIN: int = -sys.maxsize - 1

# since we only draw the bottom 20 rows on the grid, we need to have an offset

COLOR_BACKGROUND = pygame.Color("#000000")
COLOR_GRIDLINES = pygame.Color("#f5f5f5")

class TetType(Enum):
    NONE = 0
    I    = 1
    J    = 2
    L    = 3
    O    = 4
    T    = 5
    S    = 6
    Z    = 7

class TetColor(Enum):
    NONE = "#000000"
    I    = "#1D92F2"
    J    = "#D60012"
    L    = "#0927BD"
    O    = "#E8F000"
    T    = "#C500DB"
    S    = "#038C2C"
    Z    = "#D17A08"


INPUT_REPEAT_DELAY: int = 100
INPUT_REPEAT_INTERVAL: int = 50

class InputKey(Enum):
    LEFT  = pygame.K_LEFT
    DOWN  = pygame.K_DOWN
    UP    = pygame.K_UP
    RIGHT = pygame.K_RIGHT
    LROT  = pygame.K_z
    RROT  = pygame.K_x
    DROP  = pygame.K_SPACE
    PAUSE = pygame.K_p
    QUIT  = pygame.K_ESCAPE
