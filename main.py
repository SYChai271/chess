import pygame
import numpy as np
from pieces import *
from constants import *

pygame.init()


screen = pygame.display.set_mode((WIDTH, HEIGHT))
turn = 'w'
selected_piece = None
selected_square = None
selected_piece_prev = None
# BOARD constant that does not change
# BOARD constatnt is in integer form and is used to represent black and white squares on the board
BOARD = np.zeros((8, 8), dtype=int)
BOARD[:: 2, 1:: 2] = 1
BOARD[1:: 2, :: 2] = 1
# correctly orientate the board
BOARD = np.flip(BOARD, 0)
# starting position of all the pieces on the board
# (0, 0) top left
# initiate the piece objects that is imported from pieces.py
b_pieces = {'rook1': Rook((0, 0), 'b'), 'rook2': Rook((7, 0), 'b'), 'knight1': Knight((1, 0), 'b'), 'knight2': Knight((6, 0), 'b'), 'bishop1': Bishop((2, 0), 'b'), 'bishop2': Bishop((5, 0), 'b'), 'queen': Queen((3, 0), 'b'), 'king': King(
    (4, 0), 'b'), 'pawn1': Pawn((0, 1), 'b'), 'pawn2': Pawn((1, 1), 'b'), 'pawn3': Pawn((2, 1), 'b'), 'pawn4': Pawn((3, 1), 'b'), 'pawn5': Pawn((4, 1), 'b'), 'pawn6': Pawn((5, 1), 'b'), 'pawn7': Pawn((6, 1), 'b'), 'pawn8': Pawn((7, 1), 'b')}
w_pieces = {'rook1': Rook((0, 7), 'w'), 'rook2': Rook((7, 7), 'w'), 'knight1': Knight((1, 7), 'w'), 'knight2': Knight((6, 7), 'w'), 'bishop1': Bishop((2, 7), 'w'), 'bishop2': Bishop((5, 7), 'w'), 'queen': Queen((3, 7), 'w'), 'king': King(
    (4, 7), 'w'), 'pawn1': Pawn((0, 6), 'w'), 'pawn2': Pawn((1, 6), 'w'), 'pawn3': Pawn((2, 6), 'w'), 'pawn4': Pawn((3, 6), 'w'), 'pawn5': Pawn((4, 6), 'w'), 'pawn6': Pawn((5, 6), 'w'), 'pawn7': Pawn((6, 6), 'w'), 'pawn8': Pawn((7, 6), 'w')}


def on_start():
    screen.fill(BG_COLOR)
    draw_board()
    for pieces in b_pieces.values():
        draw_piece(pieces.color, pieces, pieces.pos)
    for pieces in w_pieces.values():
        draw_piece(pieces.color, pieces, pieces.pos)


def draw_board():
    global board
    board = BOARD.astype(str)
    for pieces in b_pieces.values():
        board[pieces.pos[0]][pieces.pos[1]] = pieces.color
    for pieces in w_pieces.values():
        board[pieces.pos[0]][pieces.pos[1]] = pieces.color

    # draw the board
    for i in range(8):
        for j in range(8):
            if BOARD[i, j] == 1:
                draw_square('w', (i, j))
    for i in range(8):
        for j in range(8):
            if BOARD[i, j] == 0:
                draw_square('b', (i, j))


def reverse_board():
    global board,  BOARD
    # reverse board
    # board variable is used to represent the board in string form
    # board variable is used to represent the pieces on the board (color)
    BOARD = np.flip(BOARD, 0)
    board = np.flip(board, 0)

    # draw the board
    for i in range(8):
        for j in range(8):
            if BOARD[i, j] == 1:
                draw_square('w', (i, j))
    for i in range(8):
        for j in range(8):
            if BOARD[i, j] == 0:
                draw_square('b', (i, j))

    # update pieces pos
    for pieces in b_pieces.values():
        pieces.pos = (abs(7-pieces.pos[0]), abs(7-pieces.pos[1]))
        board[pieces.pos[0]][pieces.pos[1]] = pieces.color
        draw_piece(pieces.color, pieces, pieces.pos)

    for pieces in w_pieces.values():
        pieces.pos = (abs(7-pieces.pos[0]), abs(7-pieces.pos[1]))
        board[pieces.pos[0]][pieces.pos[1]] = pieces.color
        draw_piece(pieces.color, pieces, pieces.pos)


def draw_square(color, pos):
    if color == 'b':
        pygame.draw.rect(screen, BLACK_SQUARE,
                         (pos[0] * SQUARE_SIZE, pos[1] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    else:
        pygame.draw.rect(screen, WHITE_SQUARE,
                         (pos[0] * SQUARE_SIZE, pos[1] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def draw_piece(color, piece, pos):
    screen.blit(pygame.image.load(
        piece.get_piece_img(color, piece)), (pos[0] * SQUARE_SIZE+PIECE_PADDING, pos[1] * SQUARE_SIZE+PIECE_PADDING))


def highlight_selected_piece():
    if selected_piece is not None and selected_piece_prev is None:
        screen.fill(
            SELECTED_SQUARE_COLOR, (selected_piece.pos[0] * SQUARE_SIZE, selected_piece.pos[1] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        draw_piece(selected_piece.color,
                   selected_piece, selected_piece.pos)
    elif selected_piece is not None and selected_piece_prev is not None:
        if BOARD[selected_piece_prev.pos[0]][selected_piece_prev.pos[1]] == 1:
            draw_square('w', selected_piece_prev.pos)
        else:
            draw_square('b', selected_piece_prev.pos)

        draw_piece(selected_piece_prev.color,
                   selected_piece_prev, selected_piece_prev.pos)

        screen.fill(
            SELECTED_SQUARE_COLOR, (selected_piece.pos[0] * SQUARE_SIZE, selected_piece.pos[1] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

        draw_piece(selected_piece.color,
                   selected_piece, selected_piece.pos)


def get_click_square(pos):
    if pos[0] < 640 and pos[1] < 640:
        return (pos[0] // SQUARE_SIZE, pos[1] // SQUARE_SIZE)


def get_selected_square(pos):
    global selected_square
    for pieces in b_pieces.values():
        if pieces.pos == pos and turn == 'b':
            return pieces
    for pieces in w_pieces.values():
        if pieces.pos == pos and turn == 'w':
            return pieces
    selected_square = pos


def highlight_valid_moves(moves):
    if selected_piece is not None:
        for move in moves:
            screen.fill(
                SELECTED_SQUARE_COLOR, (move[0] * SQUARE_SIZE, move[1] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            for pieces in b_pieces.values():
                if pieces.pos == move:
                    draw_piece(pieces.color, pieces, pieces.pos)
            for pieces in w_pieces.values():
                if pieces.pos == move:
                    draw_piece(pieces.color, pieces, pieces.pos)

    if selected_piece != selected_piece_prev and selected_piece.color == turn and selected_piece_prev is not None:
        moves = selected_piece_prev.valid_moves(board)
        for move in moves:
            if BOARD[move[0]][move[1]] == 1:
                draw_square('w', move)
            else:
                draw_square('b', move)


def move(pos, moves):
    global selected_square, selected_piece, selected_piece_prev, turn
    try:
        if pos in moves:
            if BOARD[selected_piece_prev.pos[0]][selected_piece_prev.pos[1]] == 1:
                draw_square('w', selected_piece_prev.pos)
                board[selected_piece_prev.pos[0]
                      ][selected_piece_prev.pos[1]] = '1'
            else:
                draw_square('b', selected_piece_prev.pos)
                board[selected_piece_prev.pos[0]
                      ][selected_piece_prev.pos[1]] = '0'
            for move in moves:
                if BOARD[move[0]][move[1]] == 1:
                    draw_square('w', move)
                else:
                    draw_square('b', move)
            draw_piece(selected_piece_prev.color,
                       selected_piece_prev, pos)

            if turn == 'b':
                turn = 'w'
                for pieces in w_pieces.values():
                    if pieces.pos != pos:
                        draw_piece(
                            pieces.color, pieces, pieces.pos)
                for key, value in w_pieces.items():
                    if value.pos == pos:
                        del w_pieces[key]
                        break
            else:
                turn = 'b'
                for pieces in b_pieces.values():
                    if pieces.pos != pos:
                        draw_piece(
                            pieces.color, pieces, pieces.pos)

                for key, value in b_pieces.items():
                    if value.pos == pos:
                        del b_pieces[key]
                        break
            try:
                selected_piece_prev.first = False
            except:
                pass
            selected_piece_prev.pos = pos
            board[selected_piece_prev.pos[0]
                  ][selected_piece_prev.pos[1]] = selected_piece_prev.color
            selected_piece_prev = None
            selected_piece = None
            selected_square = None
            if REVERSE_BOARD:
                reverse_board()
    except:
        pass


# main game logic and game loop
def main():
    global selected_piece, selected_piece_prev, selected_square
    on_start()
    _running = True
    while _running:
        # quit app if close button is pressed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                _running = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                position = get_click_square(pygame.mouse.get_pos())
                selected_piece = get_selected_square(position)
                if selected_piece is not None and selected_piece.color == turn:
                    highlight_selected_piece()
                    moves = selected_piece.valid_moves(board)
                    highlight_valid_moves(moves)
                if selected_piece_prev is not None:
                    move(selected_square, moves)
                selected_piece_prev = selected_piece
                selected_piece = None

        pygame.display.flip()


if __name__ == "__main__":
    main()
