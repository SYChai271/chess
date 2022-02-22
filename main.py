import pygame
import numpy as np
import sys
from pieces import *
from constants import *

pygame.init()


screen = pygame.display.set_mode((WIDTH, HEIGHT))


def on_start():
    reset()
    screen.fill(BG_COLOR)
    draw_board()
    update_board()
    # draw the pieces
    for pieces in b_pieces.values():
        draw_piece(pieces.color, pieces, pieces.pos)
    for pieces in w_pieces.values():
        draw_piece(pieces.color, pieces, pieces.pos)


def reset():
    # global variables
    global BOARD, board, b_pieces, w_pieces, turn, selected_piece, selected_piece_prev, selected_square, highlighted_squares
    turn = 'w'
    selected_piece = None
    selected_square = None
    selected_piece_prev = None
    highlighted_squares = []

    # BOARD constant that does not change
    # BOARD constatnt is in integer form and is used to represent black and white squares on the board
    BOARD = np.zeros((8, 8), dtype=int)
    BOARD[:: 2, 1:: 2] = 1
    BOARD[1:: 2, :: 2] = 1
    # correctly orientate the board
    BOARD = np.flip(BOARD, 0)
    board = BOARD.astype(str)
    # starting position of all the pieces on the board
    # (0, 0) top left
    # initiate the piece objects that is imported from pieces.py
    b_pieces = {'rook1': Rook((0, 0), 'b'), 'rook2': Rook((7, 0), 'b'), 'knight1': Knight((1, 0), 'b'), 'knight2': Knight((6, 0), 'b'), 'bishop1': Bishop((2, 0), 'b'), 'bishop2': Bishop((5, 0), 'b'), 'queen': Queen((3, 0), 'b'), 'king': King(
        (4, 0), 'b'), 'pawn1': Pawn((0, 1), 'b'), 'pawn2': Pawn((1, 1), 'b'), 'pawn3': Pawn((2, 1), 'b'), 'pawn4': Pawn((3, 1), 'b'), 'pawn5': Pawn((4, 1), 'b'), 'pawn6': Pawn((5, 1), 'b'), 'pawn7': Pawn((6, 1), 'b'), 'pawn8': Pawn((7, 1), 'b')}
    w_pieces = {'rook1': Rook((0, 7), 'w'), 'rook2': Rook((7, 7), 'w'), 'knight1': Knight((1, 7), 'w'), 'knight2': Knight((6, 7), 'w'), 'bishop1': Bishop((2, 7), 'w'), 'bishop2': Bishop((5, 7), 'w'), 'queen': Queen((3, 7), 'w'), 'king': King(
        (4, 7), 'w'), 'pawn1': Pawn((0, 6), 'w'), 'pawn2': Pawn((1, 6), 'w'), 'pawn3': Pawn((2, 6), 'w'), 'pawn4': Pawn((3, 6), 'w'), 'pawn5': Pawn((4, 6), 'w'), 'pawn6': Pawn((5, 6), 'w'), 'pawn7': Pawn((6, 6), 'w'), 'pawn8': Pawn((7, 6), 'w')}


def draw_board():
    # draw the board
    for i in range(8):
        for j in range(8):
            if BOARD[i, j] == 1:
                draw_square('w', (i, j))
            else:
                draw_square('b', (i, j))
    draw_borders()


def reverse_board():
    global board, BOARD
    # reverse board
    # board variable is used to represent the board in string form
    # board variable is used to represent the pieces on the board (color)
    BOARD = np.flip(BOARD, 0)
    board = BOARD.astype(str)

    # update pieces pos
    for pieces in b_pieces.values():
        pieces.pos = (abs(7-pieces.pos[0]), abs(7-pieces.pos[1]))
        board[pieces.pos[0]][pieces.pos[1]] = pieces.color

    for pieces in w_pieces.values():
        pieces.pos = (abs(7-pieces.pos[0]), abs(7-pieces.pos[1]))
        board[pieces.pos[0]][pieces.pos[1]] = pieces.color


def draw_square(color, pos):
    if color == 'b':
        pygame.draw.rect(screen, BLACK_SQUARE,
                         (pos[0] * SQUARE_SIZE, pos[1] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    elif color == 'w':
        pygame.draw.rect(screen, WHITE_SQUARE,
                         (pos[0] * SQUARE_SIZE, pos[1] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    else:
        pygame.draw.rect(screen, SELECTED_SQUARE_COLOR,
                         (pos[0] * SQUARE_SIZE, pos[1] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def draw_piece(color, piece, pos):
    screen.blit(pygame.image.load(
        piece.get_piece_img(color, piece)), (pos[0] * SQUARE_SIZE+PIECE_PADDING, pos[1] * SQUARE_SIZE+PIECE_PADDING))


def draw_borders():
    for i in range(WIDTH//SQUARE_SIZE+1):
        pygame.draw.line(screen, BORDER_COLOR,
                         (i * SQUARE_SIZE, 0), (i * SQUARE_SIZE, 640))
        pygame.draw.line(screen, BORDER_COLOR,
                         (0, i * SQUARE_SIZE), (640, i * SQUARE_SIZE))


def update_board():
    global board, highlighted_squares
    for i in range(8):
        for j in range(8):
            if BOARD[i, j] == 1:
                draw_square('w', (i, j))
            if BOARD[i, j] == 0:
                draw_square('b', (i, j))
    for square in highlighted_squares if highlighted_squares else []:
        draw_square('h', square)
    highlighted_squares = []

    for pieces in b_pieces.values():
        draw_piece(pieces.color, pieces, pieces.pos)
        board[pieces.pos[0]][pieces.pos[1]] = pieces.color + '_' + pieces.type
    for pieces in w_pieces.values():
        draw_piece(pieces.color, pieces, pieces.pos)
        board[pieces.pos[0]][pieces.pos[1]] = pieces.color + '_' + pieces.type
    draw_borders()


def highlight_selected_piece():
    global highlighted_squares
    # fill previous selected piece position back to original colour
    if selected_piece is not None and selected_piece_prev is not None:
        if BOARD[selected_piece_prev.pos[0]][selected_piece_prev.pos[1]] == 1:
            board[selected_piece_prev.pos[0]][selected_piece_prev.pos[1]] = '1'
        else:
            board[selected_piece_prev.pos[0]][selected_piece_prev.pos[1]] = '0'

    highlighted_squares.append(selected_piece.pos)


def get_clicked_square(pos):
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
    return pos


def highlight_valid_moves(moves):
    global highlighted_squares
    for move in moves:
        highlighted_squares.append(move)

    if selected_piece != selected_piece_prev and selected_piece.color == turn and selected_piece_prev is not None:
        moves_ = [move for move in selected_piece_prev.valid_moves(
            board) if move not in moves]
        for move in moves_:
            if BOARD[move[0]][move[1]] == 1:
                board[move[0]][move[1]] = '1'
            else:
                board[move[0]][move[1]] = '0'


def move(pos, moves):
    global selected_square, selected_piece, selected_piece_prev, turn, highlighted_squares
    try:
        if pos in moves:
            if BOARD[selected_piece.pos[0]][selected_piece.pos[1]] == 1:
                board[selected_piece.pos[0]
                      ][selected_piece.pos[1]] = '1'
            else:
                board[selected_piece.pos[0]
                      ][selected_piece.pos[1]] = '0'
            for move in moves:
                if BOARD[move[0]][move[1]] == 1:
                    board[selected_piece.pos[0]][selected_piece.pos[1]] = '1'
                else:
                    board[selected_piece.pos[0]][selected_piece.pos[1]] = '0'
            if turn == 'b':
                turn = 'w'
                for key, value in w_pieces.items():
                    if value.pos == pos:
                        del w_pieces[key]
                        break
            else:
                turn = 'b'
                for key, value in b_pieces.items():
                    if value.pos == pos:
                        del b_pieces[key]
                        break
            try:
                selected_piece.first = False
            except:
                pass
            selected_piece.pos = pos
            board[selected_piece.pos[0]
                  ][selected_piece.pos[1]] = selected_piece.color
            selected_piece_prev = None
            selected_piece = None
            selected_square = None
            highlighted_squares = []
            if REVERSE_BOARD:
                update_board()
                reverse_board()
    except:
        pass

# get clicked square and if it is a piece, highlight valid moves
# if it is a valid move, move the piece


def handle_pieces():
    global selected_piece, selected_piece_prev, selected_square
    position = get_clicked_square(pygame.mouse.get_pos())
    selected_square = get_selected_square(position)
    selected_piece = selected_square if selected_square in b_pieces.values(
    ) or selected_square in w_pieces.values() else selected_piece
    # deselect piece
    if selected_piece == selected_piece_prev and selected_piece == selected_square:
        selected_piece = None
    if selected_piece is not None and selected_piece.color == turn:
        highlight_selected_piece()
        moves = selected_piece.valid_moves(board)
        highlight_valid_moves(moves)
    if selected_piece is not None:
        move(selected_square, moves)
    update_board()
    selected_piece_prev = selected_piece

# main game logic and game loop


def main():
    on_start()
    _running = True
    while _running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                _running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                handle_pieces()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    on_start()

        pygame.display.flip()


if __name__ == "__main__":
    main()
