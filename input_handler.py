import pygame

from global_vars import *
from tetris import Tetris, Tetronimo

def handle_input(event: pygame.event, tetronimo: Tetronimo, tetris: Tetronimo):
    tetris.drop_disabled_timer -= 1
    tetris.rotate_disabled_timer -= 1

    for e in event:
        if e.type == pygame.QUIT:
            tetris.is_running = False
        if e.type == pygame.KEYDOWN:
            match e.key:
                case InputKey.QUIT.value:
                    tetris.is_running = False
                case InputKey.LEFT.value:
                    tetronimo.move_horizontally(InputKey.LEFT, tetris)
                case InputKey.RIGHT.value:
                    tetronimo.move_horizontally(InputKey.RIGHT, tetris)
                case InputKey.UP.value:
                    tetronimo.move_vertically(InputKey.UP, tetris)
                case InputKey.DOWN.value:
                    tetronimo.move_vertically(InputKey.DOWN, tetris)
                case InputKey.LROT.value:
                    if tetris.rotate_disabled_timer <= 0:
                        tetris.rotate_disabled_timer = DELAY_ROT
                        tetronimo.rotate(InputKey.LROT, tetris)
                case InputKey.RROT.value:
                    if tetris.rotate_disabled_timer <= 0:
                        tetris.rotate_disabled_timer = DELAY_ROT
                        tetronimo.rotate(InputKey.RROT, tetris)
                case InputKey.DROP.value:
                    if tetris.drop_disabled_timer <= 0:
                        tetris.drop_disabled_timer = DELAY_DROP
                        tetronimo.hard_drop(tetris)
                case InputKey.PAUSE.value:
                    pass
                case _:
                    pass
