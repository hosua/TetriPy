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

    # Prerender piece sizes are too big, make them smaller
    for k, v in ui_pieces.items():
        ui_pieces[k] = pygame.transform.scale(v, (PR_W, PR_H))

# Game graphics
class Graphics:
    def __init__(self, screen: pygame.display):
        self.screen = screen
        self.large_font = pygame.font.Font('./assets/font/8bitOperatorPlus-Regular.ttf', 30)
        self.med_font = pygame.font.Font('./assets/font/8bitOperatorPlus-Regular.ttf', 25)
        self.small_font = pygame.font.Font('./assets/font/8bitOperatorPlus-Regular.ttf', 20)

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

    def draw_falling_tetronimo(self, tetris):
        blocks = tetris.falling_tetronimo.get_actual_blocks_on_grid()
        color = pygame.Color(tetris.falling_tetronimo.color)
        for block in blocks:
            x, y = block
            # only render blocks in the grid
            if y >= GRID_BLOCK_OFFSET_Y:
                dx = GX + x*BW
                dy = GY + (y - GRID_BLOCK_OFFSET_Y)*BH
                rect = pygame.Rect(dx, dy, BW, BH)
                pygame.draw.rect(self.screen, color, rect)
    """
    Sizes: small, med, large
    """
    def draw_ui_text(self, text, pos: (int,int), size: str="med", color=COLOR_FONT):
        if size not in ["small", "med", "large"]:
            raise(Exception(f"Error: Invalid size parameter {size} in draw_ui_text()"))
        text_obj = None
        if size == "small":
            text_obj = self.small_font.render(text, True, color)
        elif size == "med":
            text_obj = self.med_font.render(text, True, color)
        elif size == "large":
            text_obj = self.large_font.render(text, True, color)
        text_rect = text_obj.get_rect()
        text_rect.center = pos
        self.screen.blit(text_obj, text_rect)

    def draw_ui_title(self):
        x, y = UI_TITLE_POS
        self.draw_ui_text("TetriPy", (x+35, y+20), "large", COLOR_FONT)

    def draw_ui_signature(self):
        x, y = UI_SIGNATURE_POS
        self.draw_ui_text("Made by Hoswoo", (x+35, y+20), "small", COLOR_FONT)


    def draw_ui_queue(self, tetris, count=5):
        x, y = UI_QUEUE_POS
        self.draw_ui_text("Next piece", (x+35, y+20), "med", COLOR_FONT)

        inc_x, inc_y = (0, 60)
        i_gap = 35

        for i in range(count):
            tx = x
            tet_type = tetris.queue[i].type
            if tet_type == TetType.O:
                tx += 10
            pos = (tx+inc_x, y+inc_y)
            self.screen.blit(PreRenders.ui_pieces[tet_type], pos)
            # I piece is big so give it more space
            if tet_type == TetType.I:
                y += i_gap
            y += inc_y

    def draw_ui_statistics(self, tetris):
        x, y = UI_STATS_POS
        self.draw_ui_text("Statistics", (x+35, y+20), "med", COLOR_FONT)

        tx, ty = (x-30, y+20)
        inc_x, inc_y = (0, 60)

        x += 30
        pos = (x, y+50)
        tx += 10
        ty += 60
        self.screen.blit(PreRenders.ui_pieces[TetType.I], pos)
        self.draw_ui_text(str(tetris.piece_counter[TetType.I]), (tx, ty), "med", COLOR_FONT)
        y += 90
        ty += 90

        for i in range(2, 8):
            tet_type = TetType(i)
            self.draw_ui_text(str(tetris.piece_counter[tet_type]), (tx, ty), "med", COLOR_FONT)

            ty += inc_y
            y += inc_y
            pos = (x, y)
            self.screen.blit(PreRenders.ui_pieces[tet_type], pos)

    def draw_ui_hold(self, tetris):

        x, y = UI_HOLD_POS
        tx, ty = (x+35, y+20) # text pos
        bx, by = (x-28, y+40) # box pos
        px, py = (x-20, y+50) # held piece pos
        inc_x, inc_y = (0, 60)

        self.draw_ui_text("Hold", (tx, ty), "med", COLOR_FONT)

        box_size = (PR_W+50, PR_H+50)
        bw, bh = box_size
        rect = pygame.Rect(bx, by, bw, bh)
        pygame.draw.rect(self.screen, COLOR_FONT, rect, 1)

        # don't attempt to draw the NONE type or game will go kaput
        if not tetris.hold_piece == TetType.NONE:
            tet_type = tetris.hold_piece.type

            pos = (((bw-PR_W)/2)+bx+10, ((bh-PR_H)/2)+by+15)
            # O and I piece are offset a little bit, so their cases need to
            # manually be accounted for
            if tet_type == TetType.O:
                pos = (pos[0]+10, pos[1])
            elif tet_type == TetType.I:
                pos = (pos[0], pos[1]-10)

            self.screen.blit(PreRenders.ui_pieces[tet_type], pos)
    # draws the level, score, lines cleared, tetrises achieved
    def draw_ui_other_game_statistics(self, tetris):
        x, y = UI_OTHER_STATS_POS

        self.draw_ui_text(f"Score {str(tetris.score).zfill(8)}", \
                          (x+62, y), "small", COLOR_FONT)
        self.draw_ui_text(f"Level {str(tetris.level).zfill(2)}", \
                          (x+25, y+20), "small", COLOR_FONT)
        self.draw_ui_text(f"Lines left {str(tetris.lines_until_next_level).zfill(2)}", \
                          (x+48, y+40), "small", COLOR_FONT)
        self.draw_ui_text(f"Lines {str(tetris.lines_cleared).zfill(4)}", \
                          (x+37, y+60), "small", COLOR_FONT)
        self.draw_ui_text(f"Tetris {str(tetris.tetrises).zfill(4)}", \
                          (x+42, y+80), "small", COLOR_FONT)

        # "{str(tetris.score).zfill(8)}", True, COLOR_FONT)
