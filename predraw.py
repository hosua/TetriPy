import pygame
from global_vars import *

# TODO: This is unused as of now
class Predraw:
    def __init__(self):
        self.grid_empty: pygame.display = pygame.display.set_mode([GRID_DIM_W+1, GRID_DIM_H+1])

    def draw_empty_grid(self):
        print(self.grid_empty)
        # draw vertical lines
        for x in range(0, GW+1):
            pygame.draw.line(self.grid_empty, COLOR_GRIDLINES, (x*BW, 0), (x*BW, GRID_DIM_H))
        # draw horizontal lines
        for y in range(0, GHO+1):
            pygame.draw.line(self.grid_empty, COLOR_GRIDLINES, (0, y*BH), (GRID_DIM_W, y*BH))

        pygame.image.save(self.grid_empty, 'assets/grid_empty.png')

predraw = Predraw()

predraw.draw_empty_grid()
