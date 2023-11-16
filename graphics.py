import pygame
from global_vars import *

# Game graphics
class Graphics:
    def __init__(self, screen: pygame.display):
        self.screen = screen

    def clear_screen(self):
        self.screen.fill(COLOR_BACKGROUND)

    def update_screen(self):
        pygame.display.flip()

    def draw_grid_lines(self):
        ex = GX + GRID_DIM_W # end positions
        ey = GY + GRID_DIM_H

        # draw vertical lines
        for x in range(0, GW+1):
            pygame.draw.line(self.screen, COLOR_GRIDLINES, (GX + x*BW, GY), (GX + x*BW, ey))

        # draw horizontal lines
        for y in range(0, GHO+1):
            pygame.draw.line(self.screen, COLOR_GRIDLINES, (GX, GY + y*BH), (ex, GY + y*BH))

    # draw the tetronimos that already exist on the grid
    def draw_grid_elements(self, tetris):
        grid = tetris.grid
        for y in range(0, GH):
            for x in range(0, GW):
                block = grid[y][x]
                if block == TetType.NONE:
                    continue
                dx = GX + x*BW
                dy = GY + (y-GRID_BLOCK_OFFSET_Y)*BH
                tet_type = TetType(block).name
                color = pygame.Color(TetColor[tet_type].value)
                rect = pygame.Rect(dx, dy, BW, BH)
                pygame.draw.rect(self.screen, color, rect)

    def draw_falling_tetronimo(self, tetronimo):
        blocks = tetronimo.get_actual_blocks_on_grid()
        color = pygame.Color(tetronimo.color)
        for block in blocks:
            x, y = block
            # only render blocks in the grid
            if y >= GRID_BLOCK_OFFSET_Y:
                dx = GX + x*BW
                dy = GY + (y - GRID_BLOCK_OFFSET_Y)*BH
                rect = pygame.Rect(dx, dy, BW, BH)
                pygame.draw.rect(self.screen, color, rect)

    def draw_ui_queue(self):
        pass

    def draw_ui_statistics(self):
        pass

    def draw_ui_score(self):
        pass
