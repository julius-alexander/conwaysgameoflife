"""
This project utilizes a naive implementation of Conway's Game of Life by continuously checking every cell on the grid,
every frame.
For this reason, I would not recommend adjusting the window size past (960 x 640), as it runs obnoxiously slow otherwise
This program is far from optimized, but certain improvements require more advanced techniques such as memoization,
spatial partitioning, caching, garbage collecting, and multi-threading to name a few.
HashLife is a famous algorithm used to compute large patterns efficiently, but typically does not work optimally with
interactive programs

27 June 2023 - John Garzon-Ferrer
"""


# External libraries/modules
import numpy as np
import pygame.time

# Project files/modules
from pygame_window_settings import *
from fileIO import *

# TODO =================================================================================================================
#  [ ] save generation to file output
#  [x] display generation to window, rather than console
#  [x] better file i/o (e.g., save, load from file, etc.)
#       [x] preset structures/patterns mapped to keys 1-6
#       [x] ability to save to and load from slots 7, 8, 9
#  =====================================================================================================================

print(f'\n\nCONWAY\'S GAME OF LIFE SIMULATOR\n\n'
      f'COMMANDS:\n'
      f'Left click - draw cell\n'
      f'Right click - erase cell\n'
      f'Right arrow key - step through one generation\n'
      f'Space bar - toggle simulation on/off\n'
      f's - save current state to output file game_state.json\n'
      f'l - load state from game_state.json\n'
      f'x - kill all cells\n'
      f'1 - load preset 1 (Gosper glider gun)\n'
      f'2 - load preset 2 (Glider reflector)\n'
      f'3 - load preset 3 (Glider duplicator)\n'
      f'4 - load preset 4 (Lightweight Spaceship)\n'
      f'5 - load preset 5 (Middleweight Spaceship)\n'
      f'6 - load preset 6 (Heavyweight Spaceship)\n'
      f'7 - load preset 7 (LWSS gun (3-way Gosper Gun))\n'
      f'8 - load preset 8 (SR Latch, ON, no input)\n'
      f'9 - load preset 9 (SR Latch, ON, input OFF)\n'
      f'0 - load preset 10 (SR Latch, OFF, input ON)\n')


def game_update(screen, cells_state, size, with_progress=False):
    updated_cells = np.zeros((cells_state.shape[0], cells_state.shape[1]))

    for row, col in np.ndindex(cells_state.shape):
        alive = np.sum(cells_state[row - 1:row + 2, col - 1:col + 2]) - cells_state[row, col]
        color = COLOR_BG if cells_state[row, col] == 0 else COLOR_ALIVE_NEXT

        if cells_state[row, col] == 1:
            if alive < 2 or alive > 3:
                if with_progress:
                    color = COLOR_DIE_NEXT
            elif 2 <= alive <= 3:
                updated_cells[row, col] = 1
                if with_progress:
                    color = COLOR_ALIVE_NEXT
        else:
            if alive == 3:
                updated_cells[row, col] = 1
                if with_progress:
                    color = COLOR_ALIVE_NEXT

        pygame.draw.rect(screen, color, (col * size, row * size, size - 1, size - 1))

    return updated_cells


def main():
    generation = 0
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

    cells_main = np.zeros((HEIGHT // 10, WIDTH // 10))
    screen.fill(COLOR_GRID)
    game_update(screen, cells_main, 10)
    screen.blit(display_generations(generation)[0], display_generations(generation)[1])
    pygame.display.flip()
    pygame.display.update()

    running = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            elif event.type == pygame.KEYDOWN:

                # Space bar - toggle play/pause game state
                if event.key == pygame.K_SPACE:
                    running = not running
                    game_update(screen, cells_main, 10)
                    screen.blit(display_generations(generation)[0], display_generations(generation)[1])
                    pygame.display.update()

                # 's' key - save game state
                elif event.key == pygame.K_s:
                    save_game_state(cells_main)
                    running = False
                    game_update(screen, cells_main, 10)
                    screen.blit(display_generations(generation)[0], display_generations(generation)[1])
                    pygame.display.update()
                    print('Saved to file')

                # 'l' key - load game state
                elif event.key == pygame.K_l:
                    cells_main = np.array(load_game_state("game_state.json"))
                    running = False
                    game_update(screen, cells_main, 10)
                    screen.blit(display_generations(generation)[0], display_generations(generation)[1])
                    pygame.display.update()
                    print('Loaded from file')

                # 'x' key - erase grid
                elif event.key == pygame.K_x:
                    cells_main = np.zeros((HEIGHT // 10, WIDTH // 10))
                    generation = 0
                    running = False
                    game_update(screen, cells_main, 10)
                    screen.blit(display_generations(generation)[0], display_generations(generation)[1])
                    pygame.display.update()
                    print('Erased grid')

                # Right arrow key - step through 1 generation
                elif event.key == pygame.K_RIGHT:
                    generation += 1
                    cells_main = game_update(screen, cells_main, 10, with_progress=True)
                    screen.blit(display_generations(generation)[0], display_generations(generation)[1])
                    pygame.display.update()
                    running = False

                # '1' key - load preset 1
                elif event.key == pygame.K_1:
                    cells_main = np.array(load_game_state("glider_gun.json"))
                    generation = 0
                    running = False
                    game_update(screen, cells_main, 10)
                    screen.blit(display_generations(generation)[0], display_generations(generation)[1])
                    pygame.display.update()
                    print('Loaded from file')

                # '2' key - load preset 2
                elif event.key == pygame.K_2:
                    cells_main = np.array(load_game_state("reflector.json"))
                    generation = 0
                    running = False
                    game_update(screen, cells_main, 10)
                    screen.blit(display_generations(generation)[0], display_generations(generation)[1])
                    pygame.display.update()
                    print('Loaded from file')

                # '3' key - load preset 3
                elif event.key == pygame.K_3:
                    cells_main = np.array(load_game_state("duplicator.json"))
                    generation = 0
                    running = False
                    game_update(screen, cells_main, 10)
                    screen.blit(display_generations(generation)[0], display_generations(generation)[1])
                    pygame.display.update()
                    print('Loaded from file')

                # '4' key - load preset 4
                elif event.key == pygame.K_4:
                    cells_main = np.array(load_game_state("lwss.json"))
                    generation = 0
                    running = False
                    game_update(screen, cells_main, 10)
                    screen.blit(display_generations(generation)[0], display_generations(generation)[1])
                    pygame.display.update()
                    print('Loaded from file')

                # '5' key - load preset 5
                elif event.key == pygame.K_5:
                    cells_main = np.array(load_game_state("mwss.json"))
                    generation = 0
                    running = False
                    game_update(screen, cells_main, 10)
                    screen.blit(display_generations(generation)[0], display_generations(generation)[1])
                    pygame.display.update()
                    print('Loaded from file')

                # '6' key - load preset 6
                elif event.key == pygame.K_6:
                    cells_main = np.array(load_game_state("hwss.json"))
                    generation = 0
                    running = False
                    game_update(screen, cells_main, 10)
                    screen.blit(display_generations(generation)[0], display_generations(generation)[1])
                    pygame.display.update()
                    print('Loaded from file')

                # '7' key - load preset 7
                elif event.key == pygame.K_7:
                    cells_main = np.array(load_game_state("lwss_gun.json"))
                    generation = 0
                    running = False
                    game_update(screen, cells_main, 10)
                    screen.blit(display_generations(generation)[0], display_generations(generation)[1])
                    pygame.display.update()
                    print('Loaded from file')

                # '8' key - load preset 8
                elif event.key == pygame.K_8:
                    cells_main = np.array(load_game_state("sr_latch_ON_input_none.json"))
                    generation = 0
                    running = False
                    game_update(screen, cells_main, 10)
                    screen.blit(display_generations(generation)[0],
                                display_generations(generation)[1])
                    pygame.display.update()
                    print('Loaded from file')

                # '9' key - load preset 9 (SR latch ON with off input)
                elif event.key == pygame.K_9:
                    cells_main = np.array(load_game_state("sr_latch_ON_input_off.json"))
                    generation = 0
                    running = False
                    game_update(screen, cells_main, 10)
                    screen.blit(display_generations(generation)[0],
                                display_generations(generation)[1])
                    pygame.display.update()
                    print('Loaded from file')

                # '0' key - load preset 10 (SR latch OFF with on input)
                elif event.key == pygame.K_0:
                    cells_main = np.array(load_game_state("sr_latch_OFF_input_on.json"))
                    generation = 0
                    running = False
                    game_update(screen, cells_main, 10)
                    screen.blit(display_generations(generation)[0],
                                display_generations(generation)[1])
                    pygame.display.update()
                    print('Loaded from file')

            # left mouse click - draw cell to grid
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                cells_main[pos[1] // 10, pos[0] // 10] = 1
                game_update(screen, cells_main, 10)
                screen.blit(display_generations(generation)[0], display_generations(generation)[1])
                pygame.display.update()

            # right mouse click - erase cell
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                cells_main[pos[1] // 10, pos[0] // 10] = 0
                game_update(screen, cells_main, 10)
                screen.blit(display_generations(generation)[0], display_generations(generation)[1])
                pygame.display.update()

        screen.fill(COLOR_GRID)

        if running:
            cells_main = game_update(screen, cells_main, 10, with_progress=True)
            screen.blit(display_generations(generation)[0], display_generations(generation)[1])
            pygame.display.update()
            generation += 1


if __name__ == '__main__':
    main()
