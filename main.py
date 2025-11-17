import asyncio
import pygame
import os
import sys

from global_vars import *
from tetris import Tetronimo, Tetris
from input_handler import handle_input, handle_input_paused

from graphics import Graphics


async def main():
    pygame.init()
    pygame.key.set_repeat(INPUT_REPEAT_DELAY, INPUT_REPEAT_INTERVAL)
    screen = pygame.display.set_mode([SCREEN_W, SCREEN_H])

    start_level: int = 0
    if len(sys.argv) >= 2:
        try:
            start_level = int(sys.argv[1])
        except ValueError as e:
            print(e)
            print("Assuming starting level 0.")
            start_level = 0

    tetris = Tetris(starting_level=start_level)
    clock = pygame.time.Clock()

    gfx = Graphics(screen)
    gfx.draw_grid_lines()
    gfx.update_screen()

    frame: int = 0

    tetris.last_fall_time = pygame.time.get_ticks()

    while tetris.is_running:
        if not tetris.is_paused:
            curr_time = pygame.time.get_ticks()
            if tetris.gameover():
                tetris.reset(STARTING_LEVEL, QUEUE_SIZE)
                continue

            gfx.clear_screen()
            handle_input(pygame.event.get(), tetris)

            delta_fall_time = curr_time - tetris.last_fall_time
            if delta_fall_time >= tetris.fall_interval:
                tetris.last_fall_time = curr_time
                if tetris.falling_tetronimo.is_falling:
                    tetris.fall_once()
                else:
                    tetris.place_tetronimo_on_grid()
                    num_lines_cleared: int  = tetris.clear_lines()
                    tetris.get_next_tetronimo_in_queue()

            gfx.draw_falling_tetronimo(tetris)
            gfx.draw_grid_elements(tetris)
            gfx.draw_grid_lines()

            gfx.draw_ui_title()
            gfx.draw_ui_signature()
            gfx.draw_ui_other_game_statistics(tetris)
            gfx.draw_ui_queue(tetris)
            gfx.draw_ui_statistics(tetris)
            gfx.draw_ui_hold(tetris)

        else:
            gfx.draw_ui_paused()
            handle_input_paused(pygame.event.get(), tetris)

        clock.tick(FPS)
        gfx.update_screen()

        frame += 1
        await asyncio.sleep(0)


if __name__ == "__main__":
    asyncio.run(main())
