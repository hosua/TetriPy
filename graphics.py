import pygame
from global_vars import *

class PreRenders:
    gridlines = pygame.image.load('assets/gridlines.png')
    ui_pieces = {
        TetType.I: pygame.image.load('assets/piece_I.png'),
        TetType.O: pygame.image.load('assets/piece_O.png'),
        TetType.T: pygame.image.load('assets/piece_T.png'),
        TetType.L: pygame.image.load('assets/piece_L.png'),
        TetType.J: pygame.image.load('assets/piece_J.png'),
        TetType.S: pygame.image.load('assets/piece_S.png'),
        TetType.Z: pygame.image.load('assets/piece_Z.png'),
    }

    for k, v in ui_pieces.items():
        # print(f"item: {v}")
        ui_pieces[k] = pygame.transform.scale(v, (PR_W, PR_H))

# Game graphics
class Graphics:
    def __init__(self, screen: pygame.display):
        self.screen = screen
        self.font = pygame.font.Font('./assets/font/8bitOperatorPlus-Regular.ttf', 25)

    def clear_screen(self):
        self.screen.fill(COLOR_BACKGROUND)

    def update_screen(self):
        pygame.display.flip()

    # Instead of drawing the lines every time, we can use a pre-rendered image
    def draw_grid_lines(self):
        self.screen.blit(PreRenders.gridlines, (GX, GY))

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

    def draw_ui_queue(self, tetris, count=5):
        text = self.font.render('Next Piece', True, COLOR_FONT)
        text_rect = text.get_rect()

        x, y = UI_QUEUE_POS
        inc_x, inc_y = (0, 60)
        i_gap = 35

        text_rect.center = (x+35, y+20)
        self.screen.blit(text, text_rect)

        for i in range(count):
            tx = x
            tet_type = tetris.queue[i].type
            if tet_type == TetType.O:
                tx += 10
            pos = (tx+inc_x, y+inc_y)
            self.screen.blit(PreRenders.ui_pieces[tet_type], pos)
            if tet_type == TetType.I:
                y += i_gap
            y += inc_y
