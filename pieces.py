import numpy as np
from settings import *


class Piece:
    def __init__(self, pos, color, num):
        self.pos = pos
        self.row, self.col = pos[0], pos[1]
        self.color = color
        self.type = "Piece"
        self.num = num

    def get_piece_img(self, color, piece):
        return "images/{}_{}.png".format(color.upper(), piece.type)


class Pawn(Piece):
    def __init__(self, pos, color, num):
        super().__init__(pos, color, num)
        self.en_peasant = False
        self.first = True
        self.promote = False
        self.type = "Pawn"
        self.name = self.color + "_" + self.type + str(self.num)

    def valid_moves(self, board):
        i = self.pos[0]
        j = self.pos[1]

        moves = []
        try:
            if not REVERSE_BOARD:
                if self.color == "b":
                    if i < 8:
                        p = board[i][j + 1]
                        if p[0] == "0" or p[0] == "1":
                            moves.append((i, j + 1))

                        # DIAGONAL
                        if j < 7:
                            p = board[i + 1][j + 1]
                            if p[0] != "0" and p[0] != "1":
                                if p[0] != self.color:
                                    moves.append((i + 1, j + 1))

                        if j > 0:
                            p = board[i - 1][j + 1]
                            if p[0] != "0" and p[0] != "1":
                                if p[0] != self.color:
                                    moves.append((i - 1, j + 1))

                    if self.first:
                        if i < 8:
                            p = board[i][j + 2]
                            if p[0] == "0" or p[0] == "1":
                                if board[i][j + 1] == "0" or board[i][j + 1] == "1":
                                    moves.append((i, j + 2))
                            elif p[0] != self.color:
                                moves.append((i, j + 2))

                # WHITE
                else:
                    if i >= 0:
                        p = board[i][j - 1]
                        if p[0] == "0" or p[0] == "1":
                            moves.append((i, j - 1))

                    if j < 7:
                        p = board[i - 1][j - 1]
                        if p[0] != "0" and p[0] != "1":
                            if p[0] != self.color:
                                moves.append((i - 1, j - 1))

                    if j > 0:
                        p = board[i + 1][j - 1]
                        if p[0] != "0" and p[0] != "1":
                            if p[0] != self.color:
                                moves.append((i + 1, j - 1))

                    if self.first:
                        if i >= 0:
                            p = board[i][j - 2]
                            if p[0] == "0" or p[0] == "1":
                                if board[i][j - 1] == "0" or board[i][j - 1] == "1":
                                    moves.append((i, j - 2))
                            elif p[0] != self.color:
                                moves.append((i, j - 2))
            else:
                if i >= 0:
                    p = board[i][j - 1]
                    if p[0] == "0" or p[0] == "1":
                        moves.append((i, j - 1))

                if j < 7:
                    p = board[i - 1][j - 1]
                    if p[0] != "0" and p[0] != "1":
                        if p[0] != self.color:
                            moves.append((i - 1, j - 1))

                if j > 0:
                    p = board[i + 1][j - 1]
                    if p[0] != "0" and p[0] != "1":
                        if p[0] != self.color:
                            moves.append((i + 1, j - 1))

                if self.first:
                    p = board[i][j - 2]
                    if p[0] == "0" or p[0] == "1" or p[0] != self.color:
                        if (
                            board[i][j - 1][0] == "0"
                            or board[i][j - 1][0] == "1"
                            or board[i][j - 1][0] != self.color
                        ):
                            moves.append((i, j - 2))
        except:
            pass

        return moves


class Rook(Piece):
    def __init__(self, pos, color, num):
        super().__init__(pos, color, num)
        self.first = True
        self.type = "Rook"
        self.name = self.color + "_" + self.type + str(self.num)

    def valid_moves(self, board):
        i = self.pos[0]
        j = self.pos[1]

        moves = []

        # UP
        for x in range(i - 1, -1, -1):
            p = board[x][j]
            if p[0] == "0" or p[0] == "1":
                moves.append((x, j))
            elif p[0] != self.color:
                moves.append((x, j))
                break
            else:
                break

        # DOWN
        for x in range(i + 1, 8, 1):
            p = board[x][j]
            if p[0] == "0" or p[0] == "1":
                moves.append((x, j))
            elif p[0] != self.color:
                moves.append((x, j))
                break
            else:
                break

        # LEFT
        for x in range(j - 1, -1, -1):
            p = board[i][x]
            if p[0] == "0" or p[0] == "1":
                moves.append((i, x))
            elif p[0] != self.color:
                moves.append((i, x))
                break
            else:
                break

        # RIGHT
        for x in range(j + 1, 8, 1):
            p = board[i][x]
            if p[0] == "0" or p[0] == "1":
                moves.append((i, x))
            elif p[0] != self.color:
                moves.append((i, x))
                break
            else:
                break

        return moves


class Knight(Piece):
    def __init__(self, pos, color, num):
        super().__init__(pos, color, num)
        self.type = "Knight"
        self.name = self.color + "_" + self.type + str(self.num)

    def valid_moves(self, board):
        i = self.pos[0]
        j = self.pos[1]

        moves = []

        # DOWN LEFT
        if i < 6 and j > 0:
            p = board[i + 2][j - 1]
            if p[0] == "0" or p[0] == "1":
                moves.append((i + 2, j - 1))
            elif p[0] != self.color:
                moves.append((i + 2, j - 1))

        # UP LEFT
        if i > 1 and j > 0:
            p = board[i - 2][j - 1]
            if p[0] == "0" or p[0] == "1":
                moves.append((i - 2, j - 1))
            elif p[0] != self.color:
                moves.append((i - 2, j - 1))

        # DOWN RIGHT
        if i < 6 and j < 7:
            p = board[i + 2][j + 1]
            if p[0] == "0" or p[0] == "1":
                moves.append((i + 2, j + 1))
            elif p[0] != self.color:
                moves.append((i + 2, j + 1))

        # UP RIGHT
        if i > 1 and j < 7:
            p = board[i - 2][j + 1]
            if p[0] == "0" or p[0] == "1":
                moves.append((i - 2, j + 1))
            elif p[0] != self.color:
                moves.append((i - 2, j + 1))

        if i > 0 and j > 1:
            p = board[i - 1][j - 2]
            if p[0] == "0" or p[0] == "1":
                moves.append((i - 1, j - 2))
            elif p[0] != self.color:
                moves.append((i - 1, j - 2))

        if i > 0 and j < 6:
            p = board[i - 1][j + 2]
            if p[0] == "0" or p[0] == "1":
                moves.append((i - 1, j + 2))
            elif p[0] != self.color:
                moves.append((i - 1, j + 2))

        if i < 7 and j > 1:
            p = board[i + 1][j - 2]
            if p[0] == "0" or p[0] == "1":
                moves.append((i + 1, j - 2))
            elif p[0] != self.color:
                moves.append((i + 1, j - 2))

        if i < 7 and j < 6:
            p = board[i + 1][j + 2]
            if p[0] == "0" or p[0] == "1":
                moves.append((i + 1, j + 2))
            elif p[0] != self.color:
                moves.append((i + 1, j + 2))

        return moves


class Bishop(Piece):
    def __init__(self, pos, color, num):
        super().__init__(pos, color, num)
        self.type = "Bishop"
        self.name = self.color + "_" + self.type + str(self.num)

    def valid_moves(self, board):
        i = self.pos[0]
        j = self.pos[1]

        moves = []

        # TOP RIGHT
        djL = j + 1
        djR = j - 1
        for di in range(i - 1, -1, -1):
            if djL < 8:
                p = board[di][djL]
                if p[0] == "0" or p[0] == "1":
                    moves.append((di, djL))
                elif p[0] != self.color:
                    moves.append((di, djL))
                    break
                else:
                    break
            else:
                break

            djL += 1

        for di in range(i - 1, -1, -1):
            if djR > -1:
                p = board[di][djR]
                if p[0] == "0" or p[0] == "1":
                    moves.append((di, djR))
                elif p[0] != self.color:
                    moves.append((di, djR))
                    break
                else:
                    break
            else:
                break

            djR -= 1

        # TOP LEFT
        djL = j + 1
        djR = j - 1
        for di in range(i + 1, 8):
            if djL < 8:
                p = board[di][djL]
                if p[0] == "0" or p[0] == "1":
                    moves.append((di, djL))
                elif p[0] != self.color:
                    moves.append((di, djL))
                    break
                else:
                    break
            else:
                break
            djL += 1
        for di in range(i + 1, 8):
            if djR > -1:
                p = board[di][djR]
                if p[0] == "0" or p[0] == "1":
                    moves.append((di, djR))
                elif p[0] != self.color:
                    moves.append((di, djR))
                    break
                else:
                    break
            else:
                break

            djR -= 1

        return moves


class Queen(Piece):
    def __init__(self, pos, color, num):
        super().__init__(pos, color, num)
        self.type = "Queen"
        self.name = self.color + "_" + self.type + str(self.num)

    def valid_moves(self, board):
        i = self.pos[0]
        j = self.pos[1]

        moves = []

        # TOP RIGHT
        djL = j + 1
        djR = j - 1
        for di in range(i - 1, -1, -1):
            if djL < 8:
                p = board[di][djL]
                if p[0] == "0" or p[0] == "1":
                    moves.append((di, djL))
                elif p[0] != self.color:
                    moves.append((di, djL))
                    break
                else:
                    djL = 9

            djL += 1

        for di in range(i - 1, -1, -1):
            if djR > -1:
                p = board[di][djR]
                if p[0] == "0" or p[0] == "1":
                    moves.append((di, djR))
                elif p[0] != self.color:
                    moves.append((di, djR))
                    break
                else:
                    djR = -1

            djR -= 1

        # TOP LEFT
        djL = j + 1
        djR = j - 1
        for di in range(i + 1, 8):
            if djL < 8:
                p = board[di][djL]
                if p[0] == "0" or p[0] == "1":
                    moves.append((di, djL))
                elif p[0] != self.color:
                    moves.append((di, djL))
                    break
                else:
                    djL = 9
            djL += 1
        for di in range(i + 1, 8):
            if djR > -1:
                p = board[di][djR]
                if p[0] == "0" or p[0] == "1":
                    moves.append((di, djR))
                elif p[0] != self.color:
                    moves.append((di, djR))
                    break
                else:
                    djR = -1

            djR -= 1

        # UP
        for x in range(i - 1, -1, -1):
            p = board[x][j]
            if p[0] == "0" or p[0] == "1":
                moves.append((x, j))
            elif p[0] != self.color:
                moves.append((x, j))
                break
            else:
                break

        # DOWN
        for x in range(i + 1, 8, 1):
            p = board[x][j]
            if p[0] == "0" or p[0] == "1":
                moves.append((x, j))
            elif p[0] != self.color:
                moves.append((x, j))
                break
            else:
                break

        # LEFT
        for x in range(j - 1, -1, -1):
            p = board[i][x]
            if p[0] == "0" or p[0] == "1":
                moves.append((i, x))
            elif p[0] != self.color:
                moves.append((i, x))
                break
            else:
                break

        # RIGHT
        for x in range(j + 1, 8, 1):
            p = board[i][x]
            if p[0] == "0" or p[0] == "1":
                moves.append((i, x))
            elif p[0] != self.color:
                moves.append((i, x))
                break
            else:
                break

        return moves


class King(Piece):
    def __init__(self, pos, color, num):
        super().__init__(pos, color, num)
        self.first = True
        self.type = "King"
        self.name = self.color + "_" + self.type + str(self.num)

    def valid_moves(self, board):
        i = self.pos[0]
        j = self.pos[1]

        moves = []

        if i > 0:
            # TOP LEFT
            if j > 0:
                p = board[i - 1][j - 1]
                if p[0] == "0" or p[0] == "1":
                    moves.append((i - 1, j - 1))
                elif p[0] != self.color:
                    moves.append((i - 1, j - 1))

            # TOP MIDDLE
            p = board[i - 1][j]
            if p[0] == "0" or p[0] == "1":
                moves.append((i - 1, j))
            elif p[0] != self.color:
                moves.append((i - 1, j))

            # TOP RIGHT
            if j < 7:
                p = board[i - 1][j + 1]
                if p[0] == "0" or p[0] == "1":
                    moves.append((i - 1, j + 1))
                elif p[0] != self.color:
                    moves.append((i - 1, j + 1))

        if i < 7:
            # BOTTOM LEFT
            if j > 0:
                p = board[i + 1][j - 1]
                if p[0] == "0" or p[0] == "1":
                    moves.append((i + 1, j - 1))
                elif p[0] != self.color:
                    moves.append((i + 1, j - 1))

            # BOTTOM MIDDLE
            p = board[i + 1][j]
            if p[0] == "0" or p[0] == "1":
                moves.append((i + 1, j))
            elif p[0] != self.color:
                moves.append((i + 1, j))

            # BOTTOM RIGHT
            if j < 7:
                p = board[i + 1][j + 1]
                if p[0] == "0" or p[0] == "1":
                    moves.append((i + 1, j + 1))
                elif p[0] != self.color:
                    moves.append((i + 1, j + 1))

        # MIDDLE LEFT
        if j > 0:
            p = board[i][j - 1]
            if p[0] == "0" or p[0] == "1":
                moves.append((i, j - 1))
            elif p[0] != self.color:
                moves.append((i, j - 1))

        # MIDDLE RIGHT
        if j < 7:
            p = board[i][j + 1]
            if p[0] == "0" or p[0] == "1":
                moves.append((i, j + 1))
            elif p[0] != self.color:
                moves.append((i, j + 1))

        return moves
