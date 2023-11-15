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
        self.print()

    def print(self):
        print(f"""-----------TETRONIMO-ATTRIBUTES-------------
Type: {self.type}
Falling: {self.is_falling}
Color: '{self.color}'
Origin: {self.origin}
Blocks: {self.blocks}
Actual: {self.get_actual_blocks_on_grid()}
        """)

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
    """
    param in min/max will either take the string 'x' or 'y' and return the
    value of the min/max of all blocks
    """
    def min(self, param: str) -> int:
        m: int = INT_MAX
        grid_blocks = self.get_actual_blocks_on_grid()
        for block in grid_blocks:
            if (param == 'x'):
                m = min(m, block[0])
            elif (param == 'y'):
                m = min(m, block[1])
        return m

    def max(self, param: str) -> int:
        m: int = INT_MIN
        grid_blocks = self.get_actual_blocks_on_grid()
        for block in grid_blocks:
            if (param == 'x'):
                m = max(m, block[0])
            elif (param == 'y'):
                m = max(m, block[1])
        return m

    # fall down one iteration
    def fall_once(self, tetris):
        grid = tetris.grid
        grid_blocks = self.get_actual_blocks_on_grid()
        x_min = self.min('x')
        x_max = self.max('x')
        y_max = self.max('y')

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

    def move_horizontally(self, key: InputKey, tetris):
        grid_blocks = self.get_actual_blocks_on_grid()
        can_move: bool = True

        if key == InputKey.LEFT:
            x_min: int = self.min('x')
            if not x_min == 0:
                for block in grid_blocks:
                    x, y = block
                    nx, ny = (x-1, y)
                    if not tetris.grid[ny][nx] == TetType.NONE:
                        can_move = False
                        break
                if can_move:
                    self.origin[0] -= 1
        elif key == InputKey.RIGHT:
            x_max: int = self.max('x')
            if not x_max == GW-1:
                for block in grid_blocks:
                    x, y = block
                    nx, ny = (x+1, y)
                    if not tetris.grid[ny][nx] == TetType.NONE:
                        can_move = False
                        break
                if can_move:
                    self.origin[0] += 1

    def move_vertically(self, key: InputKey, tetris):
        grid_blocks = self.get_actual_blocks_on_grid()
        can_move: bool = False

        if key == InputKey.DOWN:
            y_max: int = self.max('y')
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

        elif key == InputKey.UP:
            # Only enable when testing
            pass
            y_min: int = self.min('y')
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
            self.move_vertically(InputKey.DOWN, tetris)

class Tetris:
    def __init__(self, starting_level: int=0, queue_size: int=10):
        self.reset(starting_level, queue_size)

    def reset(self, starting_level: int, queue_size: int):
        self.grid = [[TetType.NONE] * GW for _ in range(GH)]
        self.level = starting_level
        self.fall_interval: int = 0
        self.last_fall_time: int = 0
        self.queue: list[Tetronimo] = []

        self.drop_disabled_timer: int = 0
        self.rotate_disabled_timer: int = 0

        self.populate_queue(queue_size)
        self.set_fall_interval()
        self.print_queue()


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

    def generate_rand_tetronimo(self) -> Tetronimo:
        rand_tet_type_num: int = random.randint(1, 7)
        rand_type = TetType(rand_tet_type_num)
        tetronimo = Tetronimo(rand_type)
        return tetronimo

    def populate_queue(self, n=10):
        for i in range(0, n):
            self.queue.append(self.generate_rand_tetronimo())

    def get_next_tetronimo_in_queue(self) -> Tetronimo:
        # get first tetronimo in queue
        tetronimo = self.queue.pop(0)
        # append new random tetronimo to end of queue
        self.queue.append(self.generate_rand_tetronimo())
        return tetronimo

    # When the piece stops falling, it should be placed on the actual grid
    def place_tetronimo_on_grid(self, tetronimo):
        blocks = tetronimo.get_actual_blocks_on_grid()
        tet_type = tetronimo.type
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

    # checks for and clears full lines, returns number of lines cleared
    def clear_lines(self) -> int:
        def delete_and_shift_down(yy):
            for x in range(0, GW): # delete current line
                self.grid[yy][x] = TetType.NONE
            for y in range(GRID_BLOCK_OFFSET_Y, yy):
                self.grid[y] = self.grid[y-1]

        lines_cleared: int = 0
        for y in range(GRID_BLOCK_OFFSET_Y, GH):
            line_is_full: bool = True
            for block in self.grid[y]:
                if block == TetType.NONE:
                    line_is_full = False
                    break
            if line_is_full:
                lines_cleared += 1
                delete_and_shift_down(y)

        return lines_cleared
