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
    clock = pygame.time.Clock()

    gfx = Graphics(screen)
    gfx.draw_grid_lines()
    gfx.update_screen()

    tetronimo = tetris.get_next_tetronimo_in_queue()
    tetris.piece_counter[tetronimo.type] += 1

    frame: int = 0

    # this will be used to calculate the delta to ensure the tetronimos fall 
    # at a rate independent from the FPS
    tetris.last_fall_time = round(time.time() * 1000)

    while tetris.is_running:
        curr_time = round(time.time() * 1000)
        # print(pygame.mouse.get_pos())
        if tetris.gameover():
            tetris.reset(STARTING_LEVEL, QUEUE_SIZE)

        # print(f"FRAME: {frame}")

        gfx.clear_screen()
        handle_input(pygame.event.get(), tetronimo, tetris)

        delta_fall_time = curr_time - tetris.last_fall_time
        if delta_fall_time >= tetris.fall_interval:
            tetris.last_fall_time = curr_time
            if tetronimo.is_falling:
                tetronimo.fall_once(tetris)
            else:
                tetris.place_tetronimo_on_grid(tetronimo)
                num_lines_cleared: int  = tetris.clear_lines()
                tetronimo = tetris.get_next_tetronimo_in_queue()
                tetris.piece_counter[tetronimo.type] += 1

        gfx.draw_falling_tetronimo(tetronimo)
        gfx.draw_grid_elements(tetris)
        gfx.draw_grid_lines()
        gfx.draw_ui_title()
        gfx.draw_ui_queue(tetris)
        gfx.draw_ui_statistics(tetris)
        gfx.update_screen()
        clock.tick(FPS)

        frame += 1
