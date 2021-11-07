import pygame


class Board:
    def __init__(self, rows, cols, square_size, red):
        self.rows = rows
        self.columns = cols
        self.square_size = square_size
        self.red = red
        self.board_array = [[1, 0, 1, 0, 1, 0, 1, 0],
                            [0, 1, 0, 1, 0, 1, 0, 1],
                            [1, 0, 1, 0, 1, 0, 1, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [2, 0, 2, 0, 2, 0, 2, 0],
                            [0, 2, 0, 2, 0, 2, 0, 2],
                            [2, 0, 2, 0, 2, 0, 2, 0]]

    def draw_squares(self, win):
        for row in range(self.rows):
            if row % 2 == 0:
                for col in range(0, self.columns, 2):
                    pygame.draw.rect(win, self.red, (col * self.square_size,
                                                     row * self.square_size, self.square_size, self.square_size))
            elif row % 2 == 1:
                for col in range(1, self.columns, 2):
                    pygame.draw.rect(win, self.red, (col * self.square_size,
                                                     row * self.square_size, self.square_size, self.square_size))

    def draw_pieces(self):
        pass
