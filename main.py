#!tetripy-venv/bin/python3

import pygame
import os
import sys
import time

from global_vars import *
from tetris import Tetronimo, Tetris
from input_handler import handle_input

from graphics import Graphics


if __name__ == "__main__":
    pygame.init()
    pygame.key.set_repeat(INPUT_REPEAT_DELAY, INPUT_REPEAT_INTERVAL)
    screen = pygame.display.set_mode([SCREEN_W, SCREEN_H])

    tetris = Tetris()

    gfx = Graphics(screen)
    gfx.draw_grid_lines()
    gfx.update_screen()

    # tetronimo = Tetronimo(TetType.I)
    tetronimo = tetris.get_next_tetronimo_in_queue()

    is_running: bool = True
    frame: int = 0

    # this will be used to calculate the delta to ensure the tetronimos fall 
    # at a rate independent from the FPS
    tetris.last_fall_time = round(time.time() * 1000)

    while is_running:
        curr_time = round(time.time() * 1000)
        if tetris.gameover():
            tetris.reset(STARTING_LEVEL, QUEUE_SIZE)

        # print(f"FRAME: {frame}")

        gfx.clear_screen()
        is_running = handle_input(pygame.event.get(), is_running, tetronimo, tetris)

        delta_fall_time = curr_time - tetris.last_fall_time
        if delta_fall_time >= tetris.fall_interval:
            tetris.last_fall_time = curr_time
            if tetronimo.is_falling:
                tetronimo.fall_once(tetris)
            else:
                tetris.place_tetronimo_on_grid(tetronimo)
                num_lines_cleared: int  = tetris.clear_lines()
                tetronimo = tetris.get_next_tetronimo_in_queue()

        gfx.draw_falling_tetronimo(tetronimo)
        gfx.draw_grid_elements(tetris)
        gfx.draw_grid_lines()
        gfx.update_screen()
        pygame.time.delay(FRAME_LENGTH)

        frame += 1

    pygame.quit()

