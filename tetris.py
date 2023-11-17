import os
import random

from enum import Enum
from global_vars import *

class Tetronimo:
    def __init__(self, tet_type: TetType):
        self.type: TetType = tet_type
        self.color: str = TetColor[self.type.name].value
        # this uses array instead of tuple because we need to mutate it
        self.origin: (int,int) = [5,4]
        self.blocks: list[(int,int)] = None
        self.is_falling: bool = True
        self.init_blocks()
        # self.print()

    def print(self):
        print(f"""-----------TETRONIMO-ATTRIBUTES-------------
Type: {self.type}
Falling: {self.is_falling}
Color: '{self.color}'
Origin: {self.origin}
Blocks: {self.blocks}
Actual: {self.get_actual_blocks_on_grid()}
        """)

    # When a piece gets held, it's position and rotation should be reset
    def reset(self):
        self.origin: (int,int) = [5,4]
        self.init_blocks()


    # init blocks array based on tetronimo type
    def init_blocks(self):
        # warning: match is a python3.10 feature
        match self.type:
            case TetType.I:
                self.blocks = [(0, -1), (0, 0), (0, 1), (0, 2)];
            case TetType.J:
                self.blocks = [(-1, -1), (-1, 0), (0, 0), (1, 0)];
            case TetType.L:
                self.blocks = [(-1, 0), (0, 0), (1, 0), (1, -1)];
            case TetType.O:
                self.blocks = [(-1, -1), (-1, 0), (0, -1), (0, 0)];
            case TetType.T:
                self.blocks = [(-1, 0), (0, 0), (1, 0), (0, -1)];
            case TetType.S:
                self.blocks = [(-1, 0), (0, 0), (0, -1), (1, -1)];
            case TetType.Z:
                self.blocks = [(-1, -1), (0, -1), (0, 0), (1, 0)];
            case _:
                raise Exception(f"Invalid piece type {self.type} in init_blocks()")

    # return actual block positions where the tetronimo will reside on in the grid
    def get_actual_blocks_on_grid(self) -> list[(int,int)]:
        grid_blocks: list[(int,int)] = []
        for block in self.blocks:
            grid_blocks.append((self.origin[0] + block[0], self.origin[1] + block[1]))
        return grid_blocks

    def get_min_max(self) -> (int,int,int,int):
        x_min, x_max, y_min, y_max = (INT_MAX,INT_MIN,INT_MAX,INT_MIN)
        for block in self.get_actual_blocks_on_grid():
            x, y = block
            x_min = min(x_min, x)
            x_max = max(x_max, x)
            y_min = min(y_min, y)
            y_max = max(y_max, y)

        return (x_min, x_max, y_min, y_max)


    # fall down one iteration
    def fall_once(self, tetris):
        grid = tetris.grid
        grid_blocks = self.get_actual_blocks_on_grid()
        x_min, x_max, y_min, y_max = self.get_min_max()

        # check collision against bottom of grid
        if y_max == GH-1:
            self.is_falling = False
        # check collision against other pieces already on the grid 
        else:
            for block in grid_blocks:
                x, y = block
                if not grid[y+1][x] == TetType.NONE:
                    self.is_falling = False

                if not self.is_falling:
                    break

        # move down once if the piece is still falling after all checks
        if self.is_falling:
            self.origin[1] += 1

    def move(self, key: InputKey, tetris):
        grid_blocks = self.get_actual_blocks_on_grid()
        can_move: bool = True
        x_min, x_max, y_min, y_max = self.get_min_max()

        match key:
            case InputKey.LEFT:
                if not x_min == 0:
                    for block in grid_blocks:
                        x, y = block
                        nx, ny = (x-1, y)
                        if not tetris.grid[ny][nx] == TetType.NONE:
                            can_move = False
                            break
                    if can_move:
                        self.origin[0] -= 1

            case InputKey.RIGHT:
                if not x_max == GW-1:
                    for block in grid_blocks:
                        x, y = block
                        nx, ny = (x+1, y)
                        if not tetris.grid[ny][nx] == TetType.NONE:
                            can_move = False
                            break
                    if can_move:
                        self.origin[0] += 1

            case InputKey.DOWN:
                can_move = False
                if not y_max == GH-1:
                    can_move = True
                    for block in grid_blocks:
                        x, y = block
                        nx, ny = (x, y+1)
                        if not tetris.grid[ny][nx] == TetType.NONE:
                            can_move = False
                            break

                if can_move:
                    self.origin[1] += 1
                else:
                    # immediately make next fall interval trigger in the game loop
                    tetris.last_fall_time -= tetris.fall_interval
                    self.is_falling = False

            case InputKey.UP:
                can_move = False
                # Only enable when testing
                pass # DISABLED
                if not y_min == 0:
                    for block in grid_blocks:
                        x, y = block
                        nx, ny = (x, y-1)
                        if not tetris.grid[ny][nx] == TetType.NONE:
                            can_move = False
                            break
                    if can_move:
                        self.origin[1] -= 1

    def rotate(self, key: InputKey, tetris):
        if self.type == TetType.O: # O piece does not rotate
            return
        # returns a copy of the rotated piece's positions. We use this to check
        # for any overlaps or out of bounds before actually performing the
        # rotation
        def get_rotated_copy(key: InputKey) -> list[(int,int)]:
            rotated_blocks = self.blocks.copy()
            if key == InputKey.LROT:
                for i in range(len(rotated_blocks)):
                    x, y = rotated_blocks[i]
                    rotated_blocks[i] = (y, -x)
            elif key == InputKey.RROT:
                for i in range(len(rotated_blocks)):
                    x, y = rotated_blocks[i]
                    rotated_blocks[i] = (-y, x)
            return rotated_blocks

        can_rotate: bool = True
        rotated_blocks = get_rotated_copy(key)

        for block in rotated_blocks:
            rx, ry = block
            rx += self.origin[0]
            ry += self.origin[1]
            if (rx < 0 or rx >= GW or ry < 0 or ry >= GH) or \
            not tetris.grid[ry][rx] == TetType.NONE:
                can_rotate = False
                break

        if can_rotate:
            self.blocks = rotated_blocks

    def hard_drop(self, tetris):
        while self.is_falling:
            self.move(InputKey.DOWN, tetris)

class Tetris:
    def __init__(self, starting_level: int=0, queue_size: int=10):
        self.is_running: bool = True
        self.reset(starting_level, queue_size)

    def reset(self, starting_level: int, queue_size: int):
        self.grid = [[TetType.NONE] * GW for _ in range(GH)]
        self.fall_interval: int = 0
        self.last_fall_time: int = 0
        self.queue: list[Tetronimo] = []
        self.falling_tetronimo = None

        self.level: int = starting_level
        self.score: int = 0
        self.lines_cleared: int = 0
        self.tetrises: int = 0


        self.drop_disabled_timer: int = 0
        self.rotate_disabled_timer: int = 0

        self.piece_counter = dict()
        for pc in TetType:
            self.piece_counter[pc] = 0

        self.hold_piece = TetType.NONE
        self.held_this_turn = False

        self.populate_queue(queue_size)
        self.get_next_tetronimo_in_queue()
        self.set_fall_interval()

    def hold(self):
        if not self.held_this_turn:
            self.held_this_turn = True
            self.falling_tetronimo.reset()
            if self.hold_piece == TetType.NONE:
                self.hold_piece = self.falling_tetronimo
                self.get_next_tetronimo_in_queue()
            else:
                self.hold_piece, self.falling_tetronimo = self.falling_tetronimo, self.hold_piece

    def print_grid(self):
        print("----------------GRID-STATE------------------")
        for y in range(0, GH):
            print(f"{str(y+1).rjust(2)}: ", end="")
            for x in range(0, GW):
                print(self.grid[y][x].value, end="")
            print()

    def print_queue(self):
        print("---------------QUEUE-ITEMS------------------")
        for tetronimo in self.queue:
            print(tetronimo.type, end=", ")
        print()

    def count_next_piece(self):
        self.piece_counter[self.falling_tetronimo.type] += 1

    # Set the fall speed interval based on level
    def set_fall_interval(self):
        if self.level < 9:
            self.fall_interval = (48 - (5 * (self.level + 1))) * FPS;
        elif self.level == 9:
            self.fall_interval = 6 * FPS;
        elif self.level < 13:
            self.fall_interval = 5 * FPS;
        elif self.level < 16:
            self.fall_interval = 4 * FPS;
        elif self.level < 16:
            self.fall_interval = 3 * FPS;
        elif self.level < 19:
            self.fall_interval = 2 * FPS;
        else:
            self.fall_interval = 1 * FPS;

    def fall_once(self):
        self.falling_tetronimo.fall_once(self)

    def generate_rand_tetronimo(self) -> Tetronimo:
        rand_tet_type_num: int = random.randint(1, 7)
        rand_type = TetType(rand_tet_type_num)
        tetronimo = Tetronimo(rand_type)
        return tetronimo

    def populate_queue(self, n=10):
        for i in range(0, n):
            self.queue.append(self.generate_rand_tetronimo())

    def get_next_tetronimo_in_queue(self):
        # get first tetronimo in queue
        tetronimo = self.queue.pop(0)
        # append new random tetronimo to end of queue
        self.queue.append(self.generate_rand_tetronimo())
        self.falling_tetronimo = tetronimo
        self.count_next_piece()

    # When the piece stops falling, it should be placed on the actual grid
    def place_tetronimo_on_grid(self):
        self.held_this_turn = False
        blocks = self.falling_tetronimo.get_actual_blocks_on_grid()
        tet_type = self.falling_tetronimo.type
        for block in blocks:
            x, y = block
            self.grid[y][x] = tet_type

    # Checks the grid to see if the player lost the game
    def gameover(self) -> bool:
        y: int = 4
        for x in range(0, GW):
            if not self.grid[y][x] == TetType.NONE:
                print("Game over!")
                return True
        return False

    # 1 line        2 line          3 line          4 line
	# 40 * (n + 1)  100 * (n + 1)   300 * (n + 1)   1200 * (n + 1)
    def score_calc(self, lines_cleared: int):
        self.lines_cleared += lines_cleared
        match lines_cleared:
            case 1:
                self.score += 40 * (self.level + 1)
            case 2:
                self.score += 100 * (self.level + 1)
            case 3:
                self.score += 300 * (self.level + 1)
            case 4:
                self.score += 1200 * (self.level + 1)

    # checks for and clears full lines, returns number of lines cleared
    def clear_lines(self) -> int:
        lines_cleared: int = 0
        for y in range(GRID_BLOCK_OFFSET_Y, GH):
            line_is_full: bool = True
            for block in self.grid[y]:
                if block == TetType.NONE:
                    line_is_full = False
                    break
            if line_is_full:
                # clear current line
                for x in range(GW):
                    self.grid[y][x] = TetType.NONE
                # shift lines above current y down one
                for yy in range(y, GRID_BLOCK_OFFSET_Y+1, -1):
                    self.grid[yy] = self.grid[yy-1].copy()
                lines_cleared += 1

        if lines_cleared:
            print(f"Cleared {lines_cleared} lines")
            self.score_calc(lines_cleared)
        return lines_cleared
