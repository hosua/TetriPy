import pygame

from global_vars import *
from tetris import Tetris, Tetronimo

def handle_input(event: pygame.event, tetris: Tetronimo):
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
                    tetris.falling_tetronimo.move(InputKey.LEFT, tetris)
                case InputKey.RIGHT.value:
                    tetris.falling_tetronimo.move(InputKey.RIGHT, tetris)
                case InputKey.UP.value:
                    tetris.falling_tetronimo.move(InputKey.UP, tetris)
                case InputKey.DOWN.value:
                    tetris.falling_tetronimo.move(InputKey.DOWN, tetris)
                case InputKey.LROT.value:
                    if tetris.rotate_disabled_timer <= 0:
                        tetris.rotate_disabled_timer = DELAY_ROT
                        tetris.falling_tetronimo.rotate(InputKey.LROT, tetris)
                case InputKey.RROT.value:
                    if tetris.rotate_disabled_timer <= 0:
                        tetris.rotate_disabled_timer = DELAY_ROT
                        tetris.falling_tetronimo.rotate(InputKey.RROT, tetris)
                case InputKey.DROP.value:
                    if tetris.drop_disabled_timer <= 0:
                        tetris.drop_disabled_timer = DELAY_DROP
                        tetris.falling_tetronimo.hard_drop(tetris)
                case InputKey.HOLD.value:
                    tetris.hold()
                case InputKey.PAUSE.value:
                    pass
                case _:
                    pass
