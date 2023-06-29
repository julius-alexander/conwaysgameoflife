import pygame

pygame.init()

COLOR_BG = (10, 10, 10)
COLOR_GRID = (60, 60, 60)
COLOR_DIE_NEXT = (10, 10, 10)      # 10, 10, 10
COLOR_ALIVE_NEXT = (255, 255, 255)      # 255, 255, 255

# Resolution
WIDTH, HEIGHT = 960, 640
pygame.display.set_caption('Conway\'s Game of Life')

# Font
test_font = pygame.font.Font('/Library/Fonts/Arial Unicode.ttf', 30)


def display_generations(generations):
    generations_surface = test_font.render(f'{generations}', False, (255, 0, 0))
    generations_rect = generations_surface.get_rect(center=(int(WIDTH*0.95), int(HEIGHT*0.95)))
    return generations_surface, generations_rect
