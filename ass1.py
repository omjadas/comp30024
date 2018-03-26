FREE_TILE = 0
CORNER_TILE = 1
OUT_TILE = 2
MOVES_TILL_SHRINK = 128
BORDER_TILE = 7
WHITE = "O"
BLACK = "@"


class Game:
    """
    """

    def __init__(self):
        self.read_board()

    def read_board(self):
        """Read the board layout from input"""
        layout = []
        for _ in range(8):
            layout.append(list(input()))

        self.board = Board(layout)
        return None

    def moves(self):
        print(self.board.white_player.count_moves(self.board))
        print(self.board.black_player.count_moves(self.board))
        return None

    def massacre(self):
        pass


class Board:
    """
    """

    def __init__(self, layout):
        self.layout = layout
        self.white_player = Player(self.layout, WHITE)
        self.black_player = Player(self.layout, BLACK)
        self.num_moves = 0

    def make_move2(self, move, player):
        self.layout[move[0][0]][move[0][1]] = "-"
        if player == WHITE:
            self.white_player.make_move(move)
        else:
            self.black_player.make_move(move)
        self.check_move(move, player)
        return None

    def check_move(self, move, player):
        check_around = move[1]
        row = check_around[0]
        col = check_around[1]
        enemy = BLACK if player == WHITE else WHITE
        if (self.type_of_square(row + 1, col) ==
                enemy) and self.surrounded(row + 1, col, enemy):
            self.kill((row + 1, col), enemy)
        if (self.type_of_square(row - 1, col) ==
                enemy) and self.surrounded(row - 1, col, enemy):
            self.kill((row - 1, col), enemy)
        if (self.type_of_square(row, col + 1) ==
                enemy) and self.surrounded(row, col + 1, enemy):
            self.kill((row, col + 1), enemy)
        if (self.type_of_square(row, col - 1) ==
                enemy) and self.surrounded(row, col - 1, enemy):
            self.kill((row, col - 1), enemy)
        if (self.surrounded(row, col, player)):
            self.kill(check_around, player)
        return None

    def surrounded(self, row, col, player):
        enemy = BLACK if player == WHITE else WHITE
        if (((self.type_of_square(row + 1, col) == CORNER_TILE or
              self.type_of_square(row + 1, col) == enemy) and
             (self.type_of_square(row - 1, col) == CORNER_TILE or
              self.type_of_square(row - 1, col) == enemy)) or ((self.type_of_square(row, col + 1) == CORNER_TILE or
                                                                self.type_of_square(row, col + 1) == enemy) and
                                                               (self.type_of_square(row, col - 1) == CORNER_TILE or
                                                                self.type_of_square(row, col - 1) == enemy))):
            return True
        return False

    def make_move(self, o_row, o_column, n_row, n_column, players):
        player_moved = players[0] if self.layout[o_row][o_column] == WHITE else players[1]

        player_moved.pieces[player_moved.pieces.index([o_row, o_column])] = [
            n_row, n_column]

        self.layout[n_row][n_column] = self.layout[o_row][o_column]
        self.layout[o_row][o_column] = "-"

        for i, player in enumerate(players):
            enemy = [BLACK, WHITE]
            for piece in player.pieces:
                if ((self.type_of_square(piece[0] + 1, piece[1]) == CORNER_TILE or
                     self.type_of_square(piece[0] + 1, piece[1]) == enemy[i]) and
                    (self.type_of_square(piece[0] - 1, piece[1]) == CORNER_TILE or
                     self.type_of_square(piece[0] - 1, piece[1]) == enemy[i])):
                    self.kill(piece, player)

                if ((self.type_of_square(piece[0], piece[1] + 1) == CORNER_TILE or
                     self.type_of_square(piece[0], piece[1] + 1) == enemy[i]) and
                    (self.type_of_square(piece[0], piece[1] - 1) == CORNER_TILE or
                     self.type_of_square(piece[0], piece[1] - 1) == enemy[i])):
                    self.kill(piece, player)
        return None

    def kill(self, piece, player):
        if player == WHITE:
            self.white_player.pieces.discard(piece)
        else:
            self.black_player.pieces.discard(piece)
        return None

    def type_of_square(self, row, col):
        times_shrunk = self.num_moves / MOVES_TILL_SHRINK

        if row > 7 - times_shrunk or row < 0 + times_shrunk or col > 7 - \
                times_shrunk or col < 0 + times_shrunk:
            return OUT_TILE

        if (row == 0 + times_shrunk or row == 7 - times_shrunk) and (col ==
                                                                     0 + times_shrunk or col == 7 - times_shrunk):
            return CORNER_TILE

        if self.layout[row][col] in [WHITE, BLACK]:
            return self.layout[row][col]

        if self.layout[row][col] == "-":
            return FREE_TILE


class Player:
    """
    """

    def __init__(self, layout, player):
        self.pieces = set()
        for i in range(len(layout)):
            for j in range(len(layout[i])):
                if layout[i][j] == player:
                    self.pieces.add((i, j))

    def count_moves(self, board):
        return len(self.generate_moves(board))

    def generate_moves(self, board):
        moves = []
        for i in self.pieces:
            if board.type_of_square(i[0] + 1, i[1]) == FREE_TILE:
                moves.append((i, (i[0] + 1, i[1])))
            if board.type_of_square(i[0] - 1, i[1]) == FREE_TILE:
                moves.append((i, (i[0] - 1, i[1])))
            if board.type_of_square(i[0], i[1] + 1) == FREE_TILE:
                moves.append((i, (i[0], i[1] + 1)))
            if board.type_of_square(i[0], i[1] - 1) == FREE_TILE:
                moves.append((i, (i[0], i[1] - 1)))
            if board.type_of_square(
                    i[0] + 1, i[1]) in [WHITE, BLACK] and board.type_of_square(i[0] + 2, i[1]) == FREE_TILE:
                moves.append((i, (i[0] + 2, i[1])))
            if board.type_of_square(
                    i[0] - 1, i[1]) in [WHITE, BLACK] and board.type_of_square(i[0] - 2, i[1]) == FREE_TILE:
                moves.append((i, (i[0] - 2, i[1])))
            if board.type_of_square(
                    i[0], i[1] + 1) in [WHITE, BLACK] and board.type_of_square(i[0], i[1] + 2) == FREE_TILE:
                moves.append((i, (i[0], i[1] + 2)))
            if board.type_of_square(
                    i[0], i[1] - 1) in [WHITE, BLACK] and board.type_of_square(i[0], i[1] - 2) == FREE_TILE:
                moves.append((i, (i[0], i[1] - 2)))

        return moves

    def make_move(self, move):
        self.pieces.discard(move[0])
        self.pieces.add(move[1])
        return None


class Node:
    """
    """

    def __init__(self, board, parent):
        self.board = board
        self.children = []
        self.parent = parent


game = Game()
if (input() == "Moves"):
    game.moves()
else:
    game.massacre()
