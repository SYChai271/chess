import pygame
import numpy as np
import sys
from pieces import *

pygame.init()


class App:
    def __init__(self):
        self._running = True
        self.screen = pygame.display.set_mode((640, 640))
        self.starting_position = [
            ['Rook', 'Knight', 'Bishop', 'Queen', 'King', 'Bishop', 'Knight', 'Rook'], ['Pawn' for i in range(8)]]
        self.turn = 'w'
        self.selected_piece = None
        self.selected_piece_prev = None
        self.BOARD = np.zeros((8, 8), dtype=int)
        self.BOARD[:: 2, 1:: 2] = 1
        self.BOARD[1:: 2, :: 2] = 1
        self.BOARD = np.flip(self.BOARD, 0)
        self.b_pieces = {'rook1': Rook((0, 0), 'b'), 'rook2': Rook((7, 0), 'b'), 'knight1': Knight((1, 0), 'b'), 'knight2': Knight((6, 0), 'b'), 'bishop1': Bishop((2, 0), 'b'), 'bishop2': Bishop((5, 0), 'b'), 'queen': Queen((3, 0), 'b'), 'king': King(
            (4, 0), 'b'), 'pawn1': Pawn((0, 1), 'b'), 'pawn2': Pawn((1, 1), 'b'), 'pawn3': Pawn((2, 1), 'b'), 'pawn4': Pawn((3, 1), 'b'), 'pawn5': Pawn((4, 1), 'b'), 'pawn6': Pawn((5, 1), 'b'), 'pawn7': Pawn((6, 1), 'b'), 'pawn8': Pawn((7, 1), 'b')}
        self.w_pieces = {'rook1': Rook((0, 7), 'w'), 'rook2': Rook((7, 7), 'w'), 'knight1': Knight((1, 7), 'w'), 'knight2': Knight((6, 7), 'w'), 'bishop1': Bishop((2, 7), 'w'), 'bishop2': Bishop((5, 7), 'w'), 'queen': Queen((3, 7), 'w'), 'king': King(
            (4, 7), 'w'), 'pawn1': Pawn((0, 6), 'w'), 'pawn2': Pawn((1, 6), 'w'), 'pawn3': Pawn((2, 6), 'w'), 'pawn4': Pawn((3, 6), 'w'), 'pawn5': Pawn((4, 6), 'w'), 'pawn6': Pawn((5, 6), 'w'), 'pawn7': Pawn((6, 6), 'w'), 'pawn8': Pawn((7, 6), 'w')}
        self.on_start()

    def run(self):
        while self._running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    position = self.get_click_square(pygame.mouse.get_pos())
                    self.get_selected_piece(position)
                    if self.selected_piece is not None and self.selected_piece.color == self.turn:
                        self.highlight_selected_piece()
                        moves = self.selected_piece.valid_moves(board)
                        self.highlight_valid_moves(moves)
                    if self.selected_piece_prev is not None:
                        self.move(position, moves)
                    self.selected_piece_prev = self.selected_piece
                    self.selected_piece = None

            pygame.display.flip()

    def draw_board(self):
        global board
        board = self.BOARD.astype(str)
        for pieces in self.b_pieces.values():
            board[pieces.pos[0]][pieces.pos[1]] = pieces.color
        for pieces in self.w_pieces.values():
            board[pieces.pos[0]][pieces.pos[1]] = pieces.color

        # draw the board
        for i in range(8):
            for j in range(8):
                if self.BOARD[i, j] == 1:
                    self.draw_square('w', (i, j))
        for i in range(8):
            for j in range(8):
                if self.BOARD[i, j] == 0:
                    self.draw_square('b', (i, j))

    def reverse_board(self):
        global board
        # reverse board
        self.BOARD = np.flip(self.BOARD, 0)
        board = np.flip(board, 0)

        # draw the board
        for i in range(8):
            for j in range(8):
                if self.BOARD[i, j] == 1:
                    self.draw_square('w', (i, j))
        for i in range(8):
            for j in range(8):
                if self.BOARD[i, j] == 0:
                    self.draw_square('b', (i, j))

        # update pieces pos
        for pieces in self.b_pieces.values():
            pieces.pos = (abs(7-pieces.pos[0]), abs(7-pieces.pos[1]))
            board[pieces.pos[0]][pieces.pos[1]] = pieces.color
            self.draw_piece(pieces.color, pieces.type, pieces.pos)

        for pieces in self.w_pieces.values():
            pieces.pos = (abs(7-pieces.pos[0]), abs(7-pieces.pos[1]))
            board[pieces.pos[0]][pieces.pos[1]] = pieces.color
            self.draw_piece(pieces.color, pieces.type, pieces.pos)

    def on_start(self):
        self.screen.fill((0, 74, 158))
        self.draw_board()
        for i in range(len(self.starting_position)):
            for j in range(len(self.starting_position[i])):
                self.draw_piece('b', self.starting_position[i][j], (j, i))

        _reversed = self.starting_position[::-1]
        for i in range(len(_reversed)):
            for j in range(len(_reversed[i])):
                self.draw_piece('w', _reversed[i][j], (j, i+6))

    def draw_square(self, color, pos):
        if color == 'b':
            pygame.draw.rect(self.screen, (125, 135, 150),
                             (pos[0] * 80, pos[1] * 80, 80, 80))
        else:
            pygame.draw.rect(self.screen, (232, 235, 239),
                             (pos[0] * 80, pos[1] * 80, 80, 80))

    def draw_piece(self, color, piece, pos):
        if color == 'b':
            self.screen.blit(pygame.image.load(
                './images/' + "B_" + piece + '.png'), (pos[0] * 80+10, pos[1] * 80+10))
        else:
            self.screen.blit(pygame.image.load(
                './images/' + "W_" + piece + '.png'), (pos[0] * 80+10, pos[1] * 80+10))

    def highlight_selected_piece(self):
        if self.selected_piece is not None and self.selected_piece_prev is None:
            self.screen.fill(
                (128, 128, 255), (self.selected_piece.pos[0] * 80, self.selected_piece.pos[1] * 80, 80, 80))
            self.draw_piece(self.selected_piece.color,
                            self.selected_piece.type, self.selected_piece.pos)
        elif self.selected_piece is not None and self.selected_piece_prev is not None:
            if self.BOARD[self.selected_piece_prev.pos[0]][self.selected_piece_prev.pos[1]] == 1:
                self.draw_square('w', self.selected_piece_prev.pos)
            else:
                self.draw_square('b', self.selected_piece_prev.pos)

            self.draw_piece(self.selected_piece_prev.color,
                            self.selected_piece_prev.type, self.selected_piece_prev.pos)

            self.screen.fill(
                (128, 128, 255), (self.selected_piece.pos[0] * 80, self.selected_piece.pos[1] * 80, 80, 80))

            self.draw_piece(self.selected_piece.color,
                            self.selected_piece.type, self.selected_piece.pos)

    def get_click_square(self, pos):
        if pos[0] < 640 and pos[1] < 640:
            return (pos[0] // 80, pos[1] // 80)

    def get_selected_piece(self, pos):
        for pieces in self.b_pieces.values():
            if pieces.pos == pos:
                self.selected_piece = pieces
                break
        for pieces in self.w_pieces.values():
            if pieces.pos == pos:
                self.selected_piece = pieces
                break

    def highlight_valid_moves(self, moves):
        if self.selected_piece is not None:
            for move in moves:
                self.screen.fill(
                    (128, 128, 255), (move[0] * 80, move[1] * 80, 80, 80))
                for pieces in self.b_pieces.values():
                    if pieces.pos == move:
                        self.draw_piece(pieces.color, pieces.type, pieces.pos)
                for pieces in self.w_pieces.values():
                    if pieces.pos == move:
                        self.draw_piece(pieces.color, pieces.type, pieces.pos)

        if self.selected_piece != self.selected_piece_prev and self.selected_piece.color == self.turn and self.selected_piece_prev is not None:
            moves = self.selected_piece_prev.valid_moves(board)
            for move in moves:
                if self.BOARD[move[0]][move[1]] == 1:
                    self.draw_square('w', move)
                else:
                    self.draw_square('b', move)

    def move(self, pos, moves):
        try:
            if pos in moves:
                if self.BOARD[self.selected_piece_prev.pos[0]][self.selected_piece_prev.pos[1]] == 1:
                    self.draw_square('w', self.selected_piece_prev.pos)
                    board[self.selected_piece_prev.pos[0]
                          ][self.selected_piece_prev.pos[1]] = '1'
                else:
                    self.draw_square('b', self.selected_piece_prev.pos)
                    board[self.selected_piece_prev.pos[0]
                          ][self.selected_piece_prev.pos[1]] = '0'
                for move in moves:
                    if self.BOARD[move[0]][move[1]] == 1:
                        self.draw_square('w', move)
                    else:
                        self.draw_square('b', move)
                self.draw_piece(self.selected_piece_prev.color,
                                self.selected_piece_prev.type, pos)

                if self.turn == 'b':
                    self.turn = 'w'
                    for pieces in self.w_pieces.values():
                        if pieces.pos != pos:
                            self.draw_piece(
                                pieces.color, pieces.type, pieces.pos)

                    for key, value in self.w_pieces.items():
                        if value.pos == pos:
                            del self.w_pieces[key]
                            break
                else:
                    self.turn = 'b'
                    for pieces in self.b_pieces.values():
                        if pieces.pos != pos:
                            self.draw_piece(
                                pieces.color, pieces.type, pieces.pos)

                    for key, value in self.b_pieces.items():
                        if value.pos == pos:
                            del self.b_pieces[key]
                            break
                try:
                    self.selected_piece_prev.first = False
                except:
                    pass
                self.selected_piece_prev.pos = pos
                board[self.selected_piece_prev.pos[0]
                      ][self.selected_piece_prev.pos[1]] = self.selected_piece_prev.color
                self.selected_piece_prev = None
                self.selected_piece = None
                if reverse_board:
                    self.reverse_board()
        except:
            pass


if __name__ == "__main__":
    app = App()
    app.run()
