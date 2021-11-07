import pygame

pygame.init()
pygame.font.init()

# board dimensions

WIDTH = 600
COLUMNS, ROWS = 8, 9
SQUARE_SIZE = WIDTH / COLUMNS
HEIGHT = round(WIDTH + SQUARE_SIZE)

# define colours

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
EGGSHELL = (234, 239, 250)
GREY = (153, 153, 153)
CREAM = (255, 255, 230)
NAVY = (0, 0, 102)
LIGHT_BROWN = (223, 191, 159)
SCARLET = (189, 0, 0)

# create fonts

TURN_FONT = pygame.font.SysFont('rockwell', 35)
WINNER_FONT = pygame.font.SysFont('stencil', 80)

# piece dimensions

INNER_RADIUS = SQUARE_SIZE / 2 - 10
OUTER_RADIUS = SQUARE_SIZE / 2 - 6

# gap for bottom frame

BOTTOM_GAP = 10

# Frames per second

FPS = 60

# load crown for kings

CROWN = pygame.image.load('crown.png')
CROWN_SCALED = pygame.transform.scale(CROWN, (30, 20))

# create display window

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Checkers")
WIN.fill(WHITE)

# create an array to manage locations of player pieces

board_array = [
    [1, 0, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 2, 0, 2, 0, 2, 0, 2],
    [2, 0, 2, 0, 2, 0, 2, 0],
    [0, 2, 0, 2, 0, 2, 0, 2]
]


# create a class to handle both players' pieces


class Piece:
    def __init__(self, row, column, colour):
        self.king = False
        self.row = row
        self.column = column
        self.colour = colour
        self.img = CROWN_SCALED

    def draw_piece(self, win):
        pygame.draw.circle(win, GREY, (self.column * SQUARE_SIZE + SQUARE_SIZE / 2,
                                       self.row * SQUARE_SIZE + SQUARE_SIZE / 2), OUTER_RADIUS)
        pygame.draw.circle(win, self.colour, (self.column * SQUARE_SIZE + SQUARE_SIZE / 2,
                                              self.row * SQUARE_SIZE + SQUARE_SIZE / 2), INNER_RADIUS)
        if self.king:
            win.blit(self.img, (self.column * SQUARE_SIZE + SQUARE_SIZE / 2 - self.img.get_width() / 2,
                                self.row * SQUARE_SIZE + SQUARE_SIZE / 2 - self.img.get_height() / 2))

    def move_piece(self, new_row, new_column):
        self.row = new_row
        self.column = new_column


# create a function to draw light brown square on top of a white background. This will be the playing surface.


def draw_squares(win):
    for row in range(ROWS):
        if row % 2 == 0:
            for col in range(0, COLUMNS, 2):
                pygame.draw.rect(win, LIGHT_BROWN, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        elif row % 2 == 1:
            for col in range(1, COLUMNS, 2):
                pygame.draw.rect(win, LIGHT_BROWN, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def draw_bottom_display(win, player, winner):
    pygame.draw.rect(win, GREY, (0, HEIGHT - HEIGHT / ROWS, WIDTH, SQUARE_SIZE))
    pygame.draw.rect(win, WHITE, (0 + BOTTOM_GAP, (HEIGHT - HEIGHT / ROWS) + BOTTOM_GAP,
                                  WIDTH - BOTTOM_GAP * 2, SQUARE_SIZE - BOTTOM_GAP * 2))

    if winner is None and player == 1:
        turn_text = TURN_FONT.render("Blue's turn to play", True, NAVY)
        win.blit(turn_text,
                 (WIDTH / 2 - turn_text.get_width() / 2, HEIGHT - SQUARE_SIZE / 2 - turn_text.get_height() / 2))

    if winner is None and player == 2:
        turn_text = TURN_FONT.render("Cream's turn to play", True, SCARLET)
        win.blit(turn_text,
                 (WIDTH / 2 - turn_text.get_width() / 2, HEIGHT - SQUARE_SIZE / 2 - turn_text.get_height() / 2))


def check_if_valid_piece_selected(row, column, player, piece):
    if player == 1:
        # check if selected belongs to the correct player
        if board_array[row][column] == 1:

            # ensure a potential move is on the board
            if row + 1 in range(ROWS - 1) and column - 1 in range(COLUMNS):
                # check the player's own piece is not in the potential square
                if board_array[row + 1][column - 1] == 0:
                    return True

                elif board_array[row + 1][column - 1] == 2:
                    if row + 2 in range(ROWS - 1) and column - 2 in range(COLUMNS):
                        if board_array[row + 2][column - 2] == 0:
                            return True

            if row + 1 in range(ROWS - 1) and column + 1 in range(COLUMNS):
                if board_array[row + 1][column + 1] == 0:
                    return True

                elif board_array[row + 1][column + 1] == 2:
                    if row + 2 in range(ROWS - 1) and column + 2 in range(COLUMNS):
                        if board_array[row + 2][column + 2] == 0:
                            return True

            if player == 1 and piece.king:

                # ensure a potential move is on the board
                if row - 1 in range(ROWS - 1) and column - 1 in range(COLUMNS):
                    # check the player's own piece is not in the potential square
                    if board_array[row - 1][column - 1] == 0:
                        return True

                    elif board_array[row - 1][column - 1] == 2:
                        if row - 2 in range(ROWS - 1) and column - 2 in range(COLUMNS):
                            if board_array[row - 2][column - 2] == 0:
                                return True

                if row - 1 in range(ROWS - 1) and column + 1 in range(COLUMNS):
                    if board_array[row - 1][column + 1] == 0:
                        return True

                    elif board_array[row - 1][column + 1] == 2:
                        if row - 2 in range(ROWS - 1) and column + 2 in range(COLUMNS):
                            if board_array[row - 2][column + 2] == 0:
                                return True

    elif player == 2:
        if board_array[row][column] == 2:

            # ensure a potential move is on the board
            if row - 1 in range(ROWS - 1) and column - 1 in range(COLUMNS):
                # check the player's own piece is not in the potential square
                if board_array[row - 1][column - 1] == 0:
                    return True

                elif board_array[row - 1][column - 1] == 1:
                    if row - 2 in range(ROWS - 1) and column - 2 in range(COLUMNS):
                        if board_array[row - 2][column - 2] == 0:
                            return True

            if row - 1 in range(ROWS - 1) and column + 1 in range(COLUMNS):
                if board_array[row - 1][column + 1] == 0:
                    return True

                elif board_array[row - 1][column + 1] == 1:
                    if row - 2 in range(ROWS - 1) and column + 2 in range(COLUMNS):
                        if board_array[row - 2][column + 2] == 0:
                            return True

            if player == 2 and piece.king:
                # ensure a potential move is on the board
                if row + 1 in range(ROWS - 1) and column - 1 in range(COLUMNS):
                    # check the player's own piece is not in the potential square
                    if board_array[row + 1][column - 1] == 0:
                        return True

                    elif board_array[row + 1][column - 1] == 1:
                        if row + 2 in range(ROWS - 1) and column - 2 in range(COLUMNS):
                            if board_array[row + 2][column - 2] == 0:
                                return True

                if row + 1 in range(ROWS - 1) and column + 1 in range(COLUMNS):
                    if board_array[row + 1][column + 1] == 0:
                        return True

                    elif board_array[row + 1][column + 1] == 1:
                        if row + 2 in range(ROWS - 1) and column + 2 in range(COLUMNS):
                            if board_array[row + 2][column + 2] == 0:
                                return True

    else:
        return False


def move_piece(old_row, old_column, new_row, new_column, player):
    board_array[old_row][old_column] = 0
    board_array[new_row][new_column] = player

    # check if jumped and return piece location, if so
    if abs(old_row - new_row) == 2:
        row_for_deletion = int(abs((old_row + new_row) / 2))
        column_for_deletion = int(abs((old_column + new_column)) / 2)
        board_array[row_for_deletion][column_for_deletion] = 0
        return row_for_deletion, column_for_deletion


def check_available_moves(row, col, player, piece):
    global available_moves

    available_moves.clear()

    if player == 1:
        # check the diagonal squares left
        if row + 1 in range(ROWS - 1) and col + 1 in range(COLUMNS):
            if board_array[row + 1][col + 1] == 0:
                available_moves.append((row + 1, col + 1))
            elif board_array[row + 1][col + 1] == 2:
                # check the diagonal two squares forward (left)
                if row + 2 in range(ROWS - 1) and col - 2 in range(COLUMNS):
                    if board_array[row + 2][col - 2] == 0:
                        available_moves.append((row + 2, col - 2))
                # check the diagonal two squares forward (left, then right)
                if row + 2 in range(ROWS - 1) and col + 2 in range(COLUMNS):
                    if board_array[row + 2][col + 2] == 0:
                        available_moves.append((row + 2, col + 2))

        # check the diagonal squares right
        if row + 1 in range(ROWS - 1) and col - 1 in range(COLUMNS):
            if board_array[row + 1][col - 1] == 0:
                available_moves.append((row + 1, col - 1))
            elif board_array[row + 1][col - 1] == 2:
                # check the diagonal two squares forward (right)
                if row + 2 in range(ROWS - 1) and col + 2 in range(COLUMNS):
                    if board_array[row + 2][col + 2] == 0:
                        available_moves.append((row + 2, col + 2))
                if row + 2 in range(ROWS - 1) and col - 2 in range(COLUMNS):
                    if board_array[row + 2][col - 2] == 0:
                        available_moves.append((row + 2, col - 2))

        if player == 1 and piece.king:

            if row - 1 in range(ROWS - 1) and col + 1 in range(COLUMNS):
                if board_array[row - 1][col + 1] == 0:
                    available_moves.append((row - 1, col + 1))
                elif board_array[row - 1][col + 1] == 2:
                    # check the diagonal two squares forward (left)
                    if row - 2 in range(ROWS) and col - 2 in range(COLUMNS):
                        if board_array[row - 2][col - 2] == 0:
                            available_moves.append((row - 2, col - 2))
                    # check the diagonal two squares forward (left, then right)
                    if row - 2 in range(ROWS) and col + 2 in range(COLUMNS):
                        if board_array[row - 2][col + 2] == 0:
                            available_moves.append((row - 2, col + 2))

                # check the diagonal squares right
            if row - 1 in range(ROWS - 1) and col - 1 in range(COLUMNS):
                if board_array[row - 1][col - 1] == 0:
                    available_moves.append((row - 1, col - 1))
                elif board_array[row - 1][col - 1] == 2:
                    # check the diagonal two squares forward (right)
                    if row - 2 in range(ROWS) and col + 2 in range(COLUMNS):
                        if board_array[row - 2][col + 2] == 0:
                            available_moves.append((row - 2, col + 2))
                    if row - 2 in range(ROWS) and col - 2 in range(COLUMNS):
                        if board_array[row - 2][col - 2] == 0:
                            available_moves.append((row - 2, col - 2))

    if player == 2:
        # check the diagonal squares left
        if row - 1 in range(ROWS - 1) and col + 1 in range(COLUMNS):
            if board_array[row - 1][col + 1] == 0:
                available_moves.append((row - 1, col + 1))
            elif board_array[row - 1][col + 1] == 1:
                # check the diagonal two squares forward (left)
                if row - 2 in range(ROWS) and col - 2 in range(COLUMNS):
                    if board_array[row - 2][col - 2] == 0:
                        available_moves.append((row - 2, col - 2))
                # check the diagonal two squares forward (left, then right)
                if row - 2 in range(ROWS) and col + 2 in range(COLUMNS):
                    if board_array[row - 2][col + 2] == 0:
                        available_moves.append((row - 2, col + 2))

        # check the diagonal squares right
        if row - 1 in range(ROWS - 1) and col - 1 in range(COLUMNS):
            if board_array[row - 1][col - 1] == 0:
                available_moves.append((row - 1, col - 1))
            elif board_array[row - 1][col - 1] == 1:
                # check the diagonal two squares forward (right)
                if row - 2 in range(ROWS) and col + 2 in range(COLUMNS):
                    if board_array[row - 2][col + 2] == 0:
                        available_moves.append((row - 2, col + 2))
                if row - 2 in range(ROWS) and col - 2 in range(COLUMNS):
                    if board_array[row - 2][col - 2] == 0:
                        available_moves.append((row - 2, col - 2))

        if player == 2 and piece.king:
            # check the diagonal squares left
            if row + 1 in range(ROWS - 1) and col + 1 in range(COLUMNS):
                if board_array[row + 1][col + 1] == 0:
                    available_moves.append((row + 1, col + 1))
                elif board_array[row + 1][col + 1] == 1:
                    # check the diagonal two squares forward (left)
                    if row + 2 in range(ROWS - 1) and col - 2 in range(COLUMNS):
                        if board_array[row + 2][col - 2] == 0:
                            available_moves.append((row + 2, col - 2))
                    # check the diagonal two squares forward (left, then right)
                    if row + 2 in range(ROWS - 1) and col + 2 in range(COLUMNS):
                        if board_array[row + 2][col + 2] == 0:
                            available_moves.append((row + 2, col + 2))

            # check the diagonal squares right
            if row + 1 in range(ROWS - 1) and col - 1 in range(COLUMNS):
                if board_array[row + 1][col - 1] == 0:
                    available_moves.append((row + 1, col - 1))
                elif board_array[row + 1][col - 1] == 1:
                    # check the diagonal two squares forward (right)
                    if row + 2 in range(ROWS - 1) and col + 2 in range(COLUMNS):
                        if board_array[row + 2][col + 2] == 0:
                            available_moves.append((row + 2, col + 2))
                    if row + 2 in range(ROWS - 1) and col - 2 in range(COLUMNS):
                        if board_array[row + 2][col - 2] == 0:
                            available_moves.append((row + 2, col - 2))


def check_if_further_move_available(row, column, player, piece):

    global further_available_moves

    further_available_moves = []

    if player == 1:
        # check if a potential move is on the grid
        if row + 1 in range(ROWS - 1) and column + 1 in range(COLUMNS):
            # check if there is a cream piece one row diagonally left
            if board_array[row + 1][column + 1] == 2:
                # check if the diagonal square beyond is free and append to
                # 'additional_moves_available' if so
                if row + 2 in range(ROWS - 1) and column + 2 in range(COLUMNS):
                    if board_array[row + 2][column + 2] == 0:
                        further_available_moves.append((row + 2, column + 2))

        # check if a potential move is on the grid
        if row + 1 in range(ROWS - 1) and column - 1 in range(COLUMNS):
            # check if there is a cream piece one row diagonally left
            if board_array[row + 1][column - 1] == 2:
                # check if the diagonal square beyond is free and append to
                # 'additional_moves_available' if so
                if row + 2 in range(ROWS - 1) and column - 2 in range(COLUMNS):
                    if board_array[row + 2][column - 2] == 0:
                        further_available_moves.append((row + 2, column - 2))

        # check if move available for kings
        if piece.king:
            # check if a potential move is on the grid
            if row - 1 in range(ROWS - 1) and column + 1 in range(COLUMNS):
                # check if there is a cream piece one row diagonally left
                if board_array[row - 1][column + 1] == 2:
                    # check if the diagonal square beyond is free and append to
                    # 'additional_moves_available' if so
                    if row - 2 in range(ROWS - 1) and column + 2 in range(COLUMNS):
                        if board_array[row - 2][column + 2] == 0:
                            further_available_moves.append((row - 2, column + 2))

            # check if a potential move is on the grid
            if row - 1 in range(ROWS - 1) and column - 1 in range(COLUMNS):
                # check if there is a cream piece one row diagonally left
                if board_array[row - 1][column - 1] == 2:
                    # check if the diagonal square beyond is free and append to
                    # 'additional_moves_available' if so
                    if row - 2 in range(ROWS - 1) and column - 2 in range(COLUMNS):
                        if board_array[row - 2][column - 2] == 0:
                            further_available_moves.append((row + 2, column - 2))

    if player == 2:
        # check if a potential move is on the grid
        if row - 1 in range(ROWS - 1) and column + 1 in range(COLUMNS):
            # check if there is a cream piece one row diagonally left
            if board_array[row - 1][column + 1] == 1:
                # check if the diagonal square beyond is free and append to
                # 'additional_moves_available' if so
                if row - 2 in range(ROWS - 1) and column + 2 in range(COLUMNS):
                    if board_array[row - 2][column + 2] == 0:
                        further_available_moves.append((row - 2, column + 2))

        # check if a potential move is on the grid
        if row - 1 in range(ROWS - 1) and column - 1 in range(COLUMNS):
            # check if there is a cream piece one row diagonally left
            if board_array[row - 1][column - 1] == 1:
                # check if the diagonal square beyond is free and append to
                # 'additional_moves_available' if so
                if row - 2 in range(ROWS - 1) and column - 2 in range(COLUMNS):
                    if board_array[row - 2][column - 2] == 0:
                        further_available_moves.append((row - 2, column - 2))

        if piece.king:
            # check if a potential move is on the grid
            if row + 1 in range(ROWS - 1) and column + 1 in range(COLUMNS):
                # check if there is a cream piece one row diagonally left
                if board_array[row + 1][column + 1] == 1:
                    # check if the diagonal square beyond is free and append to
                    # 'additional_moves_available' if so
                    if row + 2 in range(ROWS - 1) and column + 2 in range(COLUMNS):
                        if board_array[row + 2][column + 2] == 0:
                            further_available_moves.append((row + 2, column + 2))

            # check if a potential move is on the grid
            if row + 1 in range(ROWS - 1) and column - 1 in range(COLUMNS):
                # check if there is a cream piece one row diagonally left
                if board_array[row + 1][column - 1] == 1:
                    # check if the diagonal square beyond is free and append to
                    # 'additional_moves_available' if so
                    if row + 2 in range(ROWS - 1) and column - 2 in range(COLUMNS):
                        if board_array[row + 2][column - 2] == 0:
                            further_available_moves.append((row + 2, column - 2))

    if len(further_available_moves) == 0:
        return None

    else:
        return further_available_moves


def check_if_winner(player, piece_objects):
    pieces_left = []

    # check if any Blue pieces left - if not return Cream as winner

    if player == 1:
        for row in board_array:
            for column in row:
                if column == 1:
                    pieces_left.append(column)
        if len(pieces_left) == 0:
            return 'Cream'

    # check if any Cream pieces left - if not return Blue as winner

    elif player == 2:
        for row in board_array:
            for column in row:
                if column == 2:
                    pieces_left.append(column)
        if len(pieces_left) == 0:
            return 'Blue'

    # For each Blue piece, check if it has an available move - if not return Cream

    if player == 1:
        move_counter = 0

        for piece in piece_objects:
            check_available_moves(piece.row, piece.column, player, piece)
            move_counter += len(available_moves)

        if move_counter == 0:
            return 'Cream'

    elif player == 2:
        move_counter = 0

        for piece in piece_objects:
            check_available_moves(piece.row, piece.column, player, piece)
            move_counter += len(available_moves)

        if move_counter == 0:
            return 'Blue'

    else:
        return None


def display_winner(win, winner):
    colour = WHITE
    if winner == 'Blue':
        colour = NAVY
    elif winner == 'Cream':
        colour = SCARLET

    winning_text = WINNER_FONT.render(winner + " wins", True, colour)
    win.blit(winning_text, (WIDTH / 2 - winning_text.get_width() / 2,
                            (HEIGHT - SQUARE_SIZE) / 2 - winning_text.get_height() / 2))


def draw_window(win, player, winner, pieces, lost, row_selected, col_selected, move_selected, piece_current):
    draw_squares(win)
    draw_bottom_display(win, player, winner)

    for piece in pieces:
        piece.draw_piece(win)

    if row_selected is not None and col_selected is not None:

        if move_selected:

            if player == 1:
                pygame.draw.circle(WIN, NAVY, (col_selected * SQUARE_SIZE + SQUARE_SIZE / 2,
                                               row_selected * SQUARE_SIZE + SQUARE_SIZE / 2), INNER_RADIUS)

            elif player == 2:
                pygame.draw.circle(WIN, SCARLET, (col_selected * SQUARE_SIZE + SQUARE_SIZE / 2,
                                                  row_selected * SQUARE_SIZE + SQUARE_SIZE / 2), INNER_RADIUS)

            if piece_current.king:
                WIN.blit(CROWN_SCALED, (col_selected * SQUARE_SIZE + SQUARE_SIZE / 2 - CROWN_SCALED.get_width() / 2,
                                        row_selected * SQUARE_SIZE + SQUARE_SIZE / 2 - CROWN_SCALED.get_height() / 2))

    if lost is True:
        display_winner(win, winner)

    pygame.display.update()


def reset_game():
    global board_array
    global pieces

    # reset the board and game variables, if player presses quit

    pieces = []

    board_array = [
        [1, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 2, 0, 2, 0, 2, 0, 2],
        [2, 0, 2, 0, 2, 0, 2, 0],
        [0, 2, 0, 2, 0, 2, 0, 2]
    ]


# create  a list to contain 'piece' objects for the pieces on the board

pieces = []

# create a list to build the moves available to a piece, if a valid move selected

available_moves = []

# create a list for available moves for second or more jumps

further_available_moves = []

# create variables to handle whether a new location for a move has been selected

new_row_selected = None
new_column_selected = None
current_piece = None

# create a variable to record whether a valid move has been selected

selected_move = False

moved = False

# create a variable to handle whether an opponent has been taken, and whether a further move is applicable

jumped = False


def main():
    # set starting player

    player = 1

    # create variables to handle whether the game is over

    lost = False
    winner = None
    win_count = 0

    # create variables to handle whether a piece has been selected by a mouse click

    row_selected = None
    col_selected = None

    global new_row_selected
    global new_column_selected

    global pieces
    global board_array

    global selected_move
    global current_piece
    global jumped
    global moved

    # create 'piece' objects, given the starting position of each piece, and append to 'pieces'

    for i, row in enumerate(board_array):
        for j, column in enumerate(row):
            if column == 1:
                piece = Piece(i, j, EGGSHELL)
                pieces.append(piece)
            if column == 2:
                piece = Piece(i, j, CREAM)
                pieces.append(piece)

    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(FPS)

        draw_window(WIN, player, winner, pieces, lost, row_selected, col_selected, selected_move, current_piece)

        winner = check_if_winner(player, pieces)

        # code to freeze the 'winning text' for 3 seconds, before resetting game
        # and return the player to the 'main_menu'

        if winner is not None:
            lost = True

            win_count += 1

        if lost:
            if win_count > 3 * FPS:
                run = False
                reset_game()
            else:
                continue

        # handle player interactions with their mouse

        for event in pygame.event.get():

            # if players presses 'quit', program will return to the 'main_menu'

            if event.type == pygame.QUIT:
                run = False
                reset_game()

            if event.type == pygame.MOUSEBUTTONDOWN:

                # code to handle where the player will move

                if selected_move:
                    w = event.pos[0]
                    v = event.pos[1]
                    new_row_selected = int(v // SQUARE_SIZE)
                    new_column_selected = int(w // SQUARE_SIZE)

                # code to select the piece they want to play

                else:
                    y = event.pos[0]
                    x = event.pos[1]
                    row_selected = int(x // SQUARE_SIZE)
                    col_selected = int(y // SQUARE_SIZE)

        # code to check if player has selected a valid piece to move

        if row_selected is not None and col_selected is not None:

            # search for the selected piece in pieces, using the row and column object attributes,
            # comparing it to row_selected and column_selected

            for piece in pieces:
                if piece.row == row_selected and piece.column == col_selected:
                    current_piece = piece

            if check_if_valid_piece_selected(row_selected, col_selected, player, current_piece):
                check_available_moves(row_selected, col_selected, player, current_piece)
                selected_move = True

        # Check if a potential initial move is valid - move piece if so

        if new_row_selected is not None and new_column_selected is not None:

            if jumped:

                if (new_row_selected, new_column_selected) in further_available_moves:

                    # move the piece object in the list pieces

                    current_piece.move_piece(new_row_selected, new_column_selected)
                    moved = True

                    # 'move_piece' will alter board array to reflect the changes
                    # 'move_piece' will also return None if no opponent piece was jumped/ taken
                    # Otherwise, it will return the row and column of the piece to delete if appropriate

                    if move_piece(row_selected, col_selected, new_row_selected, new_column_selected, player) is not None:
                        row_to_del, col_to_del = move_piece(row_selected, col_selected, new_row_selected,
                                                            new_column_selected, player)
                        for piece in pieces:
                            if piece.row == row_to_del and piece.column == col_to_del:
                                pieces.remove(piece)

                else:
                    moved = False

            elif not jumped:

                if (new_row_selected, new_column_selected) in available_moves:

                    # move the piece object in the list pieces

                    current_piece.move_piece(new_row_selected, new_column_selected)
                    moved = True

                    # 'move_piece' will alter board array to reflect the changes
                    # 'move_piece' will also return None if no opponent piece was jumped/ taken
                    # Otherwise, it will return the row and column of the piece to delete if appropriate

                    if move_piece(row_selected, col_selected, new_row_selected, new_column_selected, player) is not None:
                        row_to_del, col_to_del = move_piece(row_selected, col_selected, new_row_selected,
                                                            new_column_selected, player)
                        for piece in pieces:
                            if piece.row == row_to_del and piece.column == col_to_del:
                                pieces.remove(piece)

                        # Once jumped is set to True, a check of whether another move is available will be done.

                        # Player will not change, if so, until the further move is made

                        jumped = True

                elif board_array[new_row_selected][new_column_selected] == player and jumped is False:
                    row_selected = new_row_selected
                    col_selected = new_column_selected
                    new_row_selected = None
                    new_column_selected = None

            if jumped and moved:
                if check_if_further_move_available(new_row_selected, new_column_selected, player, current_piece)\
                        is not None:

                    row_selected = new_row_selected
                    col_selected = new_column_selected

                else:
                    jumped = False
                    row_selected = None
                    col_selected = None

            # check if to be made king
            if current_piece.colour == EGGSHELL and current_piece.row == 7:
                current_piece.king = True
            elif current_piece.colour == CREAM and current_piece.row == 0:
                current_piece.king = True

            new_row_selected = None
            new_column_selected = None
            current_piece = None
            selected_move = False

            # code to change the player

            if moved is True and jumped is False:
                if player == 1:
                    player = 2
                    moved = False
                else:
                    player = 1
                    moved = False


def main_menu():
    global available_moves
    global pieces

    global new_row_selected
    global new_column_selected

    global selected_move
    global current_piece

    start_font = pygame.font.SysFont('gabriola', 60)

    run = True

    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                WIN.fill(WHITE)
                main()

        WIN.fill(WHITE)

        for row in range(ROWS):
            if row % 2 == 0:
                for col in range(0, COLUMNS, 2):
                    pygame.draw.rect(WIN, LIGHT_BROWN, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            elif row % 2 == 1:
                for col in range(1, COLUMNS, 2):
                    pygame.draw.rect(WIN, LIGHT_BROWN, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

        starting_text = start_font.render('Click to play Draughts', True, NAVY)
        WIN.blit(starting_text,
                 (WIDTH / 2 - starting_text.get_width() / 2, HEIGHT / 2 - starting_text.get_height() / 2))

        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main_menu()
