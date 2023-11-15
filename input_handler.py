import pygame

from global_vars import *
from tetris import Tetris, Tetronimo

def handle_input(event: pygame.event, is_running: bool, tetronimo: Tetronimo, tetris: Tetronimo) -> bool:
    keys_pressed = pygame.key.get_pressed()
    for e in event:
        if e.type == pygame.QUIT:
            is_running = False
        if e.type == pygame.KEYDOWN:
            match e.key:
                case InputKey.QUIT.value:
                    is_running = False
                case InputKey.LEFT.value:
                    tetronimo.move_horizontally(InputKey.LEFT, tetris)
                    if keys_pressed[InputKey.DOWN.value]:
                        tetronimo.move_vertically(InputKey.DOWN, tetris)
                case InputKey.RIGHT.value:
                    tetronimo.move_horizontally(InputKey.RIGHT, tetris)
                    if keys_pressed[InputKey.DOWN.value]:
                        tetronimo.move_vertically(InputKey.DOWN, tetris)
                case InputKey.UP.value:
                    tetronimo.move_vertically(InputKey.UP, tetris)
                case InputKey.DOWN.value:
                    tetronimo.move_vertically(InputKey.DOWN, tetris)
                    if keys_pressed[InputKey.LEFT.value]:
                        tetronimo.move_horizontally(InputKey.LEFT, tetris)
                    elif keys_pressed[InputKey.RIGHT.value]:
                        tetronimo.move_horizontally(InputKey.RIGHT, tetris)
                case InputKey.RROT.value:
                    pass
                case InputKey.LROT.value:
                    pass
                case InputKey.DROP.value:
                    pass
                case InputKey.PAUSE.value:
                    pass
                case _:
                    pass
    """
    if keys_pressed[InputKey.QUIT.value]:
        is_running = False
    if keys_pressed[InputKey.LEFT.value]:
        tetronimo.move_horizontally(InputKey.LEFT, tetris)
    if keys_pressed[InputKey.RIGHT.value]:
        tetronimo.move_horizontally(InputKey.RIGHT, tetris)
    if keys_pressed[InputKey.UP.value]:
        tetronimo.move_vertically(InputKey.UP, tetris)
    if keys_pressed[InputKey.DOWN.value]:
        tetronimo.move_vertically(InputKey.DOWN, tetris)
    """

    return is_running
