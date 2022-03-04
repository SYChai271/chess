import pygame
import numpy as np
from copy import deepcopy
from settings import *
from pieces import *


class Board:
    def __init__(self, screen):
        self.screen = screen
        self.reset()

    def reset(self):
        self.turn = 'w'
        self.selected_piece = None
        self.selected_square = None
        self.selected_piece_prev = None
        self.highlighted_squares = []
        self.board = self.get_board()
        self.game_over = False
        # starting position of all the pieces on the board
        # (0, 0) top left
        # initiate the piece objects that is imported from pieces.py
        self.w_pieces = {'rook1': Rook((0, 7), 'w', 1), 'rook2': Rook((7, 7), 'w', 2), 'knight1': Knight((1, 7), 'w', 1), 'knight2': Knight((6, 7), 'w', 2), 'bishop1': Bishop((2, 7), 'w', 1), 'bishop2': Bishop((5, 7), 'w', 2), 'queen1': Queen((3, 7), 'w', 1), 'king1': King(
            (4, 7), 'w', 1), 'pawn1': Pawn((0, 6), 'w', 1), 'pawn2': Pawn((1, 6), 'w', 2), 'pawn3': Pawn((2, 6), 'w', 3), 'pawn4': Pawn((3, 6), 'w', 4), 'pawn5': Pawn((4, 6), 'w', 5), 'pawn6': Pawn((5, 6), 'w', 6), 'pawn7': Pawn((6, 6), 'w', 7), 'pawn8': Pawn((7, 6), 'w', 8)}
        self.b_pieces = {'rook1': Rook((0, 0), 'b', 1), 'rook2': Rook((7, 0), 'b', 2), 'knight1': Knight((1, 0), 'b', 1), 'knight2': Knight((6, 0), 'b', 2), 'bishop1': Bishop((2, 0), 'b', 1), 'bishop2': Bishop((5, 0), 'b', 2), 'queen1': Queen((3, 0), 'b', 1), 'king1': King(
            (4, 0), 'b', 1), 'pawn1': Pawn((0, 1), 'b', 1), 'pawn2': Pawn((1, 1), 'b', 2), 'pawn3': Pawn((2, 1), 'b', 3), 'pawn4': Pawn((3, 1), 'b', 4), 'pawn5': Pawn((4, 1), 'b', 5), 'pawn6': Pawn((5, 1), 'b', 6), 'pawn7': Pawn((6, 1), 'b', 7), 'pawn8': Pawn((7, 1), 'b', 8)}
        self.pieces = {'w': self.w_pieces, 'b': self.b_pieces}
        self.piece_board = self.get_piece_board()

    def reverse_board(self):
        self.board = np.flip(self.board, 0)
        self.piece_board = self.board.astype(str)

        # update pieces pos
        for pieces in self.b_pieces.values():
            pieces.pos = (abs(7-pieces.pos[0]), abs(7-pieces.pos[1]))

        for pieces in self.w_pieces.values():
            pieces.pos = (abs(7-pieces.pos[0]), abs(7-pieces.pos[1]))

        self.pieces = {'w': self.w_pieces, 'b': self.b_pieces}

    def get_board(self):
        board = np.zeros((8, 8), dtype=int)
        board[:: 2, 1:: 2] = 1
        board[1:: 2, :: 2] = 1
        return board

    def get_piece_board(self):
        piece_board = self.board.astype(str)
        for _, pieces in self.pieces.items():
            for piece in pieces.values():
                piece_board[piece.pos[0]][piece.pos[1]] = piece.name
        return piece_board

    def draw_board(self):
        # draw the board
        for i in range(8):
            for j in range(8):
                if self.board[i, j] == 1:
                    self.draw_square('w', (i, j))
                else:
                    self.draw_square('b', (i, j))
        self.draw_borders()

    def draw_square(self, color, pos):
        if color == 'b':
            pygame.draw.rect(self.screen, BLACK_SQUARE,
                             (pos[0] * SQUARE_SIZE, pos[1] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        elif color == 'w':
            pygame.draw.rect(self.screen, WHITE_SQUARE,
                             (pos[0] * SQUARE_SIZE, pos[1] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        else:
            pygame.draw.rect(self.screen, SELECTED_SQUARE_COLOR,
                             (pos[0] * SQUARE_SIZE, pos[1] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def draw_piece(self, color, piece, pos):
        self.screen.blit(pygame.image.load(
            piece.get_piece_img(color, piece)), (pos[0] * SQUARE_SIZE+PIECE_PADDING, pos[1] * SQUARE_SIZE+PIECE_PADDING))

    def draw_borders(self):
        for i in range(WIDTH//SQUARE_SIZE+1):
            pygame.draw.line(self.screen, BORDER_COLOR,
                             (i * SQUARE_SIZE, 0), (i * SQUARE_SIZE, 640))
            pygame.draw.line(self.screen, BORDER_COLOR,
                             (0, i * SQUARE_SIZE), (640, i * SQUARE_SIZE))

    def update_board(self):
        for i in range(8):
            for j in range(8):
                if self.board[i, j] == 1:
                    self.draw_square('w', (i, j))
                if self.board[i, j] == 0:
                    self.draw_square('b', (i, j))
        for square in self.highlighted_squares if self.highlighted_squares else []:
            self.draw_square('h', square)
        self.highlighted_squares = []
        self.update_and_draw_pieces()
        self.draw_borders()

    def update_and_draw_pieces(self):
        """
        update all pieces on the board
        """
        for color, pieces in self.pieces.items():
            for piece in pieces.values():
                self.piece_board[piece.pos[0]][piece.pos[1]] = piece.name
                self.draw_piece(color, piece, piece.pos)

    def highlight_selected_piece(self):
        self.highlighted_squares.append(self.selected_piece.pos)

    def highlight_valid_moves(self, moves):
        for move in moves:
            self.highlighted_squares.append(move)

    def get_clicked_square(self, pos):
        if pos[0] < 640 and pos[1] < 640:
            return (pos[0] // SQUARE_SIZE, pos[1] // SQUARE_SIZE)

    def get_selected_square(self, pos):
        """
        returns selected piece at pos 
        if no pieces at pos, return pos of clicked square
        """
        for color, pieces in self.pieces.items():
            for piece in pieces.values():
                if piece.pos == pos and self.turn == color:
                    return piece
        return pos

    # undo previous move
    def take_back(self):
        if REVERSE_BOARD:
            self.reverse_board()
        self.update_board()
        # iterate through board and update pieces
        for i in range(len(self.previous_board)):
            for j in range(len(self.previous_board[i])):
                s = self.previous_board[i][j]
                if self.piece_board[i][j] != s:
                    if s[0] == 'b':
                        for piece in self.b_pieces.values():
                            if piece.name == s:
                                piece.pos = (i, j)
                    elif s[0] == 'w':
                        for piece in self.w_pieces.values():
                            if piece.name == s:
                                piece.pos = (i, j)
                    else:
                        continue
        self.piece_board = self.previous_board
        self.turn = 'w' if self.turn == 'b' else 'b'
        self.update_board()

    def check_moves(self, moves):
        """
        make a copy of self as a new board
        """
        rejected_moves = []
        for i in range(len(moves)):
            _piece_board = deepcopy(self.piece_board)
            _board = deepcopy(self.board)
            _pieces = deepcopy(self.pieces)
            _piece = _pieces[self.turn].get(
                self.selected_piece.type.lower()+str(self.selected_piece.num))
            _piece_board, _piece = self._do_move(
                _piece, moves[i], _piece_board, _board)
            if self.is_in_check(self.turn, _piece_board, _pieces):
                rejected_moves.append(moves[i])
        moves = [move for move in moves if move not in rejected_moves]
        return moves

    def _do_move(self, piece, move, piece_board, board):
        """
        returns a new board with the move applied
        """
        piece_board[piece.pos[0]][piece.pos[1]
                                  ] = board[piece.pos[0]][piece.pos[1]]
        piece_board[move[0]][move[1]] = piece.name
        piece.pos = move
        return piece_board, piece

    def get_king(self, color, pieces):
        for piece in pieces[color].values():
            if piece.type == 'King':
                return piece

    def get_enemy(self, color):
        return 'b' if color == 'w' else 'w'

    def get_all_possible_moves(self, color, piece_board, pieces):
        result = []
        for piece in pieces[color].values():
            moves = piece.valid_moves(piece_board)
            result += moves
        return result

    def is_in_check(self, color, piece_board, pieces):
        king = self.get_king(color, pieces)
        enemy = self.get_enemy(color)
        return king.pos in self.get_all_possible_moves(enemy, piece_board, pieces)

    def checkmate(self, color):
        if self.check_moves(self.get_all_possible_moves(color, self.piece_board, self.pieces)) == [] and self.is_in_check(color, self.piece_board, self.pieces):
            return True
        return False

    def stalemate(self, color):
        if self.check_moves(self.get_all_possible_moves(color, self.piece_board, self.pieces)) == [] and not self.is_in_check(color, self.piece_board, self.pieces):
            return True
        return False

    def get_winner(self):
        if self.checkmate('w'):
            return 'Black'
        if self.checkmate('b'):
            return 'White'
        return None

    def get_draw(self):
        if self.stalemate('w') and self.stalemate('b'):
            return True
        return False

    # check if the game is over
    def _game_over(self):
        return True if self.get_winner() or self.get_draw() else False

    def move(self, pos):
        self.previous_board = np.copy(self.piece_board)
        if self.board[self.selected_piece.pos[0]][self.selected_piece.pos[1]] == 1:
            self.piece_board[self.selected_piece.pos[0]
                                ][self.selected_piece.pos[1]] = '1'
        else:
            self.piece_board[self.selected_piece.pos[0]
                                ][self.selected_piece.pos[1]] = '0'
        if self.turn == 'b':
            self.turn = 'w'
            for key, value in self.w_pieces.items():
                if value.pos == pos:
                    del self.w_pieces[key]
                    break
        else:
            self.turn = 'b'
            for key, value in self.b_pieces.items():
                if value.pos == pos:
                    del self.b_pieces[key]
                    break
        try:
            self.selected_piece.first = False
        except:
            pass
        self.selected_piece.pos = pos
        self.piece_board[pos[0]][pos[1]] = self.selected_piece.name
        self.update_board()
        self.highlighted_squares = []
        if self._game_over():
            self.game_over = True
            return
        self.selected_piece_prev = None
        self.selected_piece = None
        self.selected_square = None
        if REVERSE_BOARD:
            self.reverse_board()


    def handle_click(self):
        position = self.get_clicked_square(pygame.mouse.get_pos())
        self.selected_square = self.get_selected_square(position)
        self.selected_piece = self.selected_square if self.selected_square in self.b_pieces.values(
        ) or self.selected_square in self.w_pieces.values() else self.selected_piece
        # deselect piece
        if self.selected_piece == self.selected_piece_prev and self.selected_piece == self.selected_square:
            self.selected_piece = None
        if self.selected_piece and self.selected_piece.color == self.turn and self.selected_piece:
            self.highlight_selected_piece()
            moves = self.check_moves(
                self.selected_piece.valid_moves(self.piece_board))
            self.highlight_valid_moves(moves)
        if self.selected_piece and self.selected_square in moves:
            self.move(self.selected_square)
        self.update_board()
        self.selected_piece_prev = self.selected_piece
