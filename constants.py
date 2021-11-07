import pygame

# board dimensions

WIDTH, HEIGHT = 600, 600
COLUMNS, ROWS = 8, 8
SQUARE_SIZE = WIDTH / COLUMNS

# define colours

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREY = (179, 179, 179)

# piece dimensions

INNER_RADIUS = SQUARE_SIZE / 2 - 5
OUTER_RADIUS = SQUARE_SIZE / 2 - 3