import pygame
import numpy as np
import sys
from copy import deepcopy
from pieces import *
from constants import *

pygame.init()


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Chess')


def on_start():
    reset()
    screen.fill(BG_COLOR)
    draw_board()
    update_board()


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
    w_pieces = {'rook1': Rook((0, 7), 'w', 1), 'rook2': Rook((7, 7), 'w', 2), 'knight1': Knight((1, 7), 'w', 1), 'knight2': Knight((6, 7), 'w', 2), 'bishop1': Bishop((2, 7), 'w', 1), 'bishop2': Bishop((5, 7), 'w', 2), 'queen1': Queen((3, 7), 'w', 1), 'king1': King(
        (4, 7), 'w', 1), 'pawn1': Pawn((0, 6), 'w', 1), 'pawn2': Pawn((1, 6), 'w', 2), 'pawn3': Pawn((2, 6), 'w', 3), 'pawn4': Pawn((3, 6), 'w', 4), 'pawn5': Pawn((4, 6), 'w', 5), 'pawn6': Pawn((5, 6), 'w', 6), 'pawn7': Pawn((6, 6), 'w', 7), 'pawn8': Pawn((7, 6), 'w', 8)}
    b_pieces = {'rook1': Rook((0, 0), 'b', 1), 'rook2': Rook((7, 0), 'b', 2), 'knight1': Knight((1, 0), 'b', 1), 'knight2': Knight((6, 0), 'b', 2), 'bishop1': Bishop((2, 0), 'b', 1), 'bishop2': Bishop((5, 0), 'b', 2), 'queen1': Queen((3, 0), 'b', 1), 'king1': King(
        (4, 0), 'b', 1), 'pawn1': Pawn((0, 1), 'b', 1), 'pawn2': Pawn((1, 1), 'b', 2), 'pawn3': Pawn((2, 1), 'b', 3), 'pawn4': Pawn((3, 1), 'b', 4), 'pawn5': Pawn((4, 1), 'b', 5), 'pawn6': Pawn((5, 1), 'b', 6), 'pawn7': Pawn((6, 1), 'b', 7), 'pawn8': Pawn((7, 1), 'b', 8)}


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
        board[pieces.pos[0]][pieces.pos[1]] = pieces.name
    for pieces in w_pieces.values():
        draw_piece(pieces.color, pieces, pieces.pos)
        board[pieces.pos[0]][pieces.pos[1]] = pieces.name
    draw_borders()


def highlight_selected_piece():
    global highlighted_squares
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


# undo previous move
def take_back():
    global board, turn
    reverse_board()
    update_board()
    # iterate through board and update pieces
    for i in range(len(previous_board)):
        for j in range(len(previous_board[i])):
            s = previous_board[i][j]
            if board[i][j] != s:
                if s[0] == 'b':
                    for piece in b_pieces.values():
                        if piece.name == s:
                            piece.pos = (i, j)
                elif s[0] == 'w':
                    for piece in w_pieces.values():
                        if piece.name == s:
                            piece.pos = (i, j)
                else:
                    continue
    board = previous_board
    turn = 'w' if turn == 'b' else 'b'
    update_board()

# check if move will cause king to be checked


def check_moves(moves):
    rejected_moves = []
    for i in range(len(moves)):
        _board = board.copy()
        _w_pieces = deepcopy(w_pieces)
        _b_pieces = deepcopy(b_pieces)
        if turn == 'w':
            piece = _w_pieces.get(
                selected_piece.type.lower()+str(selected_piece.num))
        else:
            piece = _b_pieces.get(
                selected_piece.type.lower()+str(selected_piece.num))
        _board, piece = _do_move(piece, moves[i], _board)
        if is_in_check(turn, board, _w_pieces, _b_pieces):
            rejected_moves.append(moves[i])
    moves = [move for move in moves if move not in rejected_moves]
    return moves


def _do_move(piece, move, _board):
    _board[piece.pos[0]][piece.pos[1]] = str(BOARD[piece.pos[0]][piece.pos[1]])
    _board[move[0]][move[1]] = piece.name
    piece.pos = move
    return _board, piece


def get_king(color, w_pieces, b_pieces):
    if color == 'w':
        return w_pieces.get('king1')
    else:
        return b_pieces.get('king1')


def get_enemy(color):
    return 'b' if color == 'w' else 'w'


def get_all_possible_moves(color, board, w_pieces, b_pieces):
    result = []
    if color == 'w':
        for piece in w_pieces.values():
            result += piece.valid_moves(board)
    else:
        for piece in b_pieces.values():
            result += piece.valid_moves(board)
    return result


def is_in_check(color, board, w_pieces, b_pieces):
    king = get_king(color, w_pieces, b_pieces)
    enemy = get_enemy(color)
    return king.pos in get_all_possible_moves(enemy, board, w_pieces, b_pieces)


def checkmate(color):
    if get_all_possible_moves(color, board, w_pieces, b_pieces) == [] and is_in_check(color, board, w_pieces, b_pieces):
        return True
    return False


def move(pos, moves):
    global selected_square, selected_piece, selected_piece_prev, previous_board, turn, highlighted_squares
    try:
        if pos in moves:
            previous_board = np.copy(board)
            if BOARD[selected_piece.pos[0]][selected_piece.pos[1]] == 1:
                board[selected_piece.pos[0]
                      ][selected_piece.pos[1]] = '1'
            else:
                board[selected_piece.pos[0]
                      ][selected_piece.pos[1]] = '0'
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
                  ][selected_piece.pos[1]] = selected_piece.name
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


def handle_click():
    global selected_piece, selected_piece_prev, selected_square
    position = get_clicked_square(pygame.mouse.get_pos())
    selected_square = get_selected_square(position)
    selected_piece = selected_square if selected_square in b_pieces.values(
    ) or selected_square in w_pieces.values() else selected_piece
    # deselect piece
    if selected_piece == selected_piece_prev and selected_piece == selected_square:
        selected_piece = None
    if selected_piece and selected_piece.color == turn and selected_piece:
        highlight_selected_piece()
        moves = check_moves(selected_piece.valid_moves(board))
        highlight_valid_moves(moves)
    if selected_piece:
        move(selected_square, moves)
        if checkmate(turn):
            print('white' if turn == 'b' else 'black' + ' wins!')
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
                handle_click()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    _running = False
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_r:
                    on_start()
                if event.key == pygame.K_u:
                    take_back()

        pygame.display.flip()


if __name__ == "__main__":
    main()
