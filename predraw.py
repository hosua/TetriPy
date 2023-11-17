import pygame
from global_vars import *

"""
Code in this file is not used for the game, it's used to draw images to blit in the game.
"""
class Predraw:
    def __init__(self):
        self.grid_empty: pygame.Surface = pygame.Surface([GRID_DIM_W+1, GRID_DIM_H+1], pygame.SRCALPHA)
        self.piece_buffer: pygame.Surface = pygame.Surface([PB_W, PB_H], pygame.SRCALPHA)

    def init_blocks(self, tet_type):
        # warning: match is a python3.10 feature
        match tet_type:
            case TetType.I:
                return [(0, -1), (0, 0), (0, 1), (0, 2)];
            case TetType.J:
                return [(-1, -1), (-1, 0), (0, 0), (1, 0)];
            case TetType.L:
                return [(-1, 0), (0, 0), (1, 0), (1, -1)];
            case TetType.O:
                return [(-1, -1), (-1, 0), (0, -1), (0, 0)];
            case TetType.T:
                return [(-1, 0), (0, 0), (1, 0), (0, -1)];
            case TetType.S:
                return [(-1, 0), (0, 0), (0, -1), (1, -1)];
            case TetType.Z:
                return [(-1, -1), (0, -1), (0, 0), (1, 0)];
            case _:
                raise Exception(f"Invalid piece type {self.type} in init_blocks()")
        return None

    def draw_empty_grid(self):
        # self.grid_empty.fill((0,0,0,0))
        print(self.grid_empty)
        # draw vertical lines
        for x in range(0, GW+1):
            pygame.draw.line(self.grid_empty, COLOR_GRIDLINES, (x*BW, 0), (x*BW, GRID_DIM_H))
        # draw horizontal lines
        for y in range(0, GHO+1):
            pygame.draw.line(self.grid_empty, COLOR_GRIDLINES, (0, y*BH), (GRID_DIM_W, y*BH))

        pygame.image.save(self.grid_empty, 'assets/gridlines.png')

    def draw_all_pieces(self):
        origin = [1,1]
        ox, oy = origin
        for i in range(1, 8):
            self.piece_buffer.fill((0,0,0,0))
            tet_type = TetType(i)
            blocks = self.init_blocks(tet_type)
            color = pygame.Color(TetColor[tet_type.name].value)
            for block in blocks:
                bx, by = block
                x = (ox + bx) * PW
                y = (oy + by) * PH
                rect = pygame.Rect(x, y, PW, PH)
                pygame.draw.rect(self.piece_buffer, color, rect)

            pygame.image.save(self.piece_buffer, f'assets/piece_{tet_type.name}.png')

if __name__ == "__main__":
    predraw = Predraw()
    predraw.draw_empty_grid()
    predraw.draw_all_pieces()
