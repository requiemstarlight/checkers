import pygame

pygame.init()
pygame.font.init()

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

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Checkers")
WIN.fill(WHITE)

board_array = [[[1, False], [0, False], [1, False], [0, False], [1, False], [0, False], [1, False], [0, False]],
               [[0, False], [1, False], [0, False], [1, False], [0, False], [1, False], [0, False], [1, False]],
               [[1, False], [0, False], [1, False], [0, False], [1, False], [0, False], [1, False], [0, False]],
               [[0, False], [0, False], [0, False], [0, False], [0, False], [0, False], [0, False], [0, False]],
               [[0, False], [0, True], [0, False], [0, False], [0, False], [0, False], [0, False], [0, False]],
               [[0, False], [2, False], [0, False], [2, False], [0, False], [2, False], [0, False], [2, False]],
               [[2, False], [0, False], [2, False], [0, False], [2, False], [0, False], [2, False], [0, False]],
               [[0, False], [2, False], [0, False], [2, False], [0, False], [2, False], [0, False], [2, False]]]


def draw_squares(win):
    for row in range(ROWS):
        if row % 2 == 0:
            for col in range(0, COLUMNS, 2):
                pygame.draw.rect(win, LIGHT_BROWN, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        elif row % 2 == 1:
            for col in range(1, COLUMNS, 2):
                pygame.draw.rect(win, LIGHT_BROWN, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def draw_pieces(win):
    for row in range(len(board_array)):
        for col in range(len(board_array)):
            if board_array[row][col][0] == 1:
                pygame.draw.circle(win, GREY, (col * SQUARE_SIZE + SQUARE_SIZE / 2,
                                               row * SQUARE_SIZE + SQUARE_SIZE / 2), OUTER_RADIUS)
                pygame.draw.circle(win, EGGSHELL, (col * SQUARE_SIZE + SQUARE_SIZE / 2,
                                                   row * SQUARE_SIZE + SQUARE_SIZE / 2), INNER_RADIUS)
                if board_array[row][col][1]:
                    win.blit(CROWN_SCALED, (col * SQUARE_SIZE + SQUARE_SIZE / 2 - CROWN_SCALED.get_width() / 2,
                                            row * SQUARE_SIZE + SQUARE_SIZE / 2 - CROWN_SCALED.get_height() / 2))

            if board_array[row][col][0] == 2:
                pygame.draw.circle(win, GREY, (col * SQUARE_SIZE + SQUARE_SIZE / 2,
                                               row * SQUARE_SIZE + SQUARE_SIZE / 2), OUTER_RADIUS)
                pygame.draw.circle(win, CREAM, (col * SQUARE_SIZE + SQUARE_SIZE / 2,
                                                row * SQUARE_SIZE + SQUARE_SIZE / 2), INNER_RADIUS)
                if board_array[row][col][1]:
                    if board_array[row][col][1]:
                        win.blit(CROWN_SCALED, (col * SQUARE_SIZE + SQUARE_SIZE / 2 - CROWN_SCALED.get_width() / 2,
                                                row * SQUARE_SIZE + SQUARE_SIZE / 2 - CROWN_SCALED.get_height() / 2))


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


def check_if_valid_square_selected(row, column, player):
    if player == 1:
        # check if selected belongs to the correct player
        if board_array[row][column][0] == 1:
            # ensure the potential move is on the board
            if row + 1 in range(ROWS) and column - 1 in range(COLUMNS):
                # check the player's own piece is not in the potential square
                if board_array[row + 1][column - 1][0] != 1:
                    return True

            if row + 1 in range(ROWS) and column + 1 in range(COLUMNS):
                if board_array[row + 1][column + 1][0] != 1:
                    return True

    elif player == 2:
        if board_array[row][column][0] == 2:
            if row - 1 in range(ROWS) and column - 1 in range(COLUMNS):
                if board_array[row - 1][column - 1][0] != 2:
                    return True

            if row - 1 in range(ROWS) and column + 1 in range(COLUMNS):
                if board_array[row - 1][column + 1][0] != 2:
                    return True

    else:
        return False


def move_piece(win, old_row, old_column, new_row, new_column, player):
    board_array[old_row][old_column][0] = 0
    board_array[new_row][new_column][0] = player

    # check if jumped and remove piece if so
    if abs(old_row - new_row) == 2:
        board_array[int(abs((old_row + new_row) / 2))][int(abs((old_column + new_column)) / 2)][0] = 0
        if player == 1:
            pygame.draw.circle(win, GREY, (15 + SQUARE_SIZE / 2, HEIGHT - SQUARE_SIZE / 2), OUTER_RADIUS)
            pygame.draw.circle(win, CREAM, (15 + SQUARE_SIZE / 2, HEIGHT - SQUARE_SIZE / 2), INNER_RADIUS)
        elif player == 2:
            pygame.draw.circle(win, GREY, (15 + SQUARE_SIZE / 2, HEIGHT - SQUARE_SIZE / 2), OUTER_RADIUS)
            pygame.draw.circle(win, EGGSHELL, (15 + SQUARE_SIZE / 2, HEIGHT - SQUARE_SIZE / 2), INNER_RADIUS)


def check_available_moves(row, col, player):
    global available_moves

    available_moves.clear()

    if player == 1:
        # check the diagonal squares left
        if row + 1 in range(ROWS - 1) and col + 1 in range(COLUMNS):
            if board_array[row + 1][col + 1][0] == 0:
                available_moves.append((row + 1, col + 1))
            elif board_array[row + 1][col + 1][0] == 2:
                # check the diagonal two squares forward (left)
                if row + 2 in range(ROWS) and col - 2 in range(COLUMNS):
                    if board_array[row + 2][col - 2][0] == 0:
                        available_moves.append((row + 2, col - 2))
                # check the diagonal two squares forward (left, then right)
                if row + 2 in range(ROWS) and col + 2 in range(COLUMNS):
                    if board_array[row + 2][col + 2][0] == 0:
                        available_moves.append((row + 2, col - 2))

        # check the diagonal squares right
        if row + 1 in range(ROWS - 1) and col - 1 in range(COLUMNS):
            if board_array[row + 1][col - 1][0] == 0:
                available_moves.append((row + 1, col - 1))
            elif board_array[row + 1][col - 1][0] == 2:
                # check the diagonal two squares forward (right)
                if row + 2 in range(ROWS) and col + 2 in range(COLUMNS):
                    if board_array[row + 2][col + 2][0] == 0:
                        available_moves.append((row + 2, col + 2))
                if row + 2 in range(ROWS) and col - 2 in range(COLUMNS):
                    if board_array[row + 2][col - 2][0] == 0:
                        available_moves.append((row + 2, col - 2))

    if player == 2:
        # check the diagonal squares left
        if row - 1 in range(ROWS - 1) and col + 1 in range(COLUMNS):
            if board_array[row - 1][col + 1][0] == 0:
                available_moves.append((row - 1, col + 1))
            elif board_array[row - 1][col + 1][0] == 1:
                # check the diagonal two squares forward (left)
                if row - 2 in range(ROWS) and col - 2 in range(COLUMNS):
                    if board_array[row - 2][col - 2][0] == 0:
                        available_moves.append((row - 2, col - 2))
                # check the diagonal two squares forward (left, then right)
                if row - 2 in range(ROWS) and col + 2 in range(COLUMNS):
                    if board_array[row - 2][col + 2][0] == 0:
                        available_moves.append((row - 2, col - 2))

        # check the diagonal squares right
        if row - 1 in range(ROWS - 1) and col - 1 in range(COLUMNS):
            if board_array[row - 1][col - 1][0] == 0:
                available_moves.append((row - 1, col - 1))
            elif board_array[row - 1][col - 1][0] == 1:
                # check the diagonal two squares forward (right)
                if row - 2 in range(ROWS) and col + 2 in range(COLUMNS):
                    if board_array[row - 2][col + 2][0] == 0:
                        available_moves.append((row - 2, col + 2))
                if row - 2 in range(ROWS) and col - 2 in range(COLUMNS):
                    if board_array[row - 2][col - 2][0] == 0:
                        available_moves.append((row - 2, col - 2))


available_moves = []

# create global variable to monitor the number of pieces and kings left, in order for the AI to calculate the best moves

blue_pieces = cream_pieces = 12
blue_kings = cream_kings = 0


def main():
    player = 1
    winner = None

    row_selected = None
    col_selected = None
    new_row_selected = None
    new_column_selected = None
    selected_move = False

    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

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

        draw_squares(WIN)
        draw_pieces(WIN)
        draw_bottom_display(WIN, player, winner)

        # code to check if player has selected a valid piece to move

        if row_selected is not None and col_selected is not None:
            if check_if_valid_square_selected(row_selected, col_selected, player):
                if player == 1:
                    pygame.draw.circle(WIN, NAVY, (col_selected * SQUARE_SIZE + SQUARE_SIZE / 2,
                                                   row_selected * SQUARE_SIZE + SQUARE_SIZE / 2), INNER_RADIUS)
                elif player == 2:
                    pygame.draw.circle(WIN, SCARLET, (col_selected * SQUARE_SIZE + SQUARE_SIZE / 2,
                                                      row_selected * SQUARE_SIZE + SQUARE_SIZE / 2), INNER_RADIUS)
                check_available_moves(row_selected, col_selected, player)

                selected_move = True

        # code to move the piece

        if new_row_selected is not None and new_column_selected is not None:
            if (new_row_selected, new_column_selected) in available_moves:
                move_piece(WIN, row_selected, col_selected, new_row_selected, new_column_selected, player)

                new_row_selected = None
                new_column_selected = None
                selected_move = False

                # code to change the player
                if player == 1:
                    player = 2
                else:
                    player = 1

            elif board_array[new_row_selected][new_column_selected][0] == player:
                row_selected = new_row_selected
                col_selected = new_column_selected
                new_row_selected = None
                new_column_selected = None

        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
