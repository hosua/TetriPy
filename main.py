#!tetripy-venv/bin/python3

import pygame
import os
import sys

from tetris import Tetronimo, Tetris
from global_vars import *

from graphics import Graphics

TICK_LENGTH: int = 200

def handle_input(event: pygame.event, is_running: bool) -> bool:
    for e in event:
        if e.type == pygame.QUIT:
            is_running = False
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                is_running = False
    return is_running


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode([SCREEN_W, SCREEN_H])

    tetris = Tetris()

    gfx = Graphics(screen)
    gfx.draw_grid_lines()
    gfx.update_screen()

    # tetronimo = Tetronimo(TetType.I)
    tetronimo = tetris.get_next_tetronimo_in_queue()

    is_running: bool = True
    frame: int = 0
    while is_running:
        if tetris.gameover():
            tetris.reset()

        print(f"FRAME: {frame}")
        gfx.clear_screen()
        is_running = handle_input(pygame.event.get(), is_running)

        if tetronimo.is_falling:
            tetronimo.fall_once(tetris)
        else:
            tetris.place_tetronimo_on_grid(tetronimo)
            tetronimo = tetris.get_next_tetronimo_in_queue()

        gfx.draw_falling_tetronimo(tetronimo)
        gfx.draw_grid_elements(tetris)
        gfx.draw_grid_lines()
        gfx.update_screen()
        pygame.time.delay(TICK_LENGTH)
        frame += 1

    pygame.quit()

