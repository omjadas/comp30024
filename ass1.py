import copy
import time

FREE_TILE = 0
CORNER_TILE = 1
OUT_TILE = 2
MOVES_TILL_SHRINK = 128
BORDER_TILE = 7
WHITE = "O"
BLACK = "@"
MAX_DEPTH = 5


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
        print(
            self.board.white_player.count_moves(
                self.board.white_player.pieces,
                self.board.layout))
        print(
            self.board.black_player.count_moves(
                self.board.black_player.pieces,
                self.board.layout))
        return None

    def massacre(self):
        start = time.time()
        while not Board.game_finished(self.board.layout):
            # print(self.board.layout)
            move = Player.minimax(
                self.board.layout,
                self.board.white_player,
                self.board.black_player)

            # print(move)
            # print(move[-2][0])

            for m in move[-2]:
                print("{} -> {}".format(m[0],m[1]))
                Board.make_move(m, self.board.layout,
                                self.board.white_player, self.board.black_player)
        end = time.time()
        print(end-start)
        return None


class Board:
    """
    """

    def __init__(self, layout):
        self.layout = layout
        self.white_player = Player(self.layout, WHITE)
        self.black_player = Player(self.layout, BLACK)
        self.num_moves = 0

    @staticmethod
    def make_move(move, layout, player1, player2):
        layout[move[0][0]][move[0][1]] = "-"
        layout[move[1][0]][move[1][1]] = player1.symbol
        Player.make_move(player1.pieces, move)
        Board.check_move(move, layout, player1, player2)
        return None

    @staticmethod
    def check_move(move, layout, player1, player2):
        check_around = move[1]
        row = check_around[0]
        col = check_around[1]
        if (Board.type_of_square(row + 1, col, layout) ==
                player2.symbol) and Board.surrounded(row + 1, col, player2.symbol, layout):
            Board.kill((row + 1, col), player2, layout)
        if (Board.type_of_square(row - 1, col, layout) ==
                player2.symbol) and Board.surrounded(row - 1, col, player2.symbol, layout):
            Board.kill((row - 1, col), player2, layout)
        if (Board.type_of_square(row, col + 1, layout) ==
                player2.symbol) and Board.surrounded(row, col + 1, player2.symbol, layout):
            Board.kill((row, col + 1), player2, layout)
        if (Board.type_of_square(row, col - 1, layout) ==
                player2.symbol) and Board.surrounded(row, col - 1, player2.symbol, layout):
            Board.kill((row, col - 1), player2, layout)
        if (Board.surrounded(row, col, player1, layout)):
            Board.kill(check_around, player1, layout)
        return None

    @staticmethod
    def surrounded(row, col, player, layout):
        enemy = BLACK if player == WHITE else WHITE
        if (((Board.type_of_square(row + 1, col, layout) == CORNER_TILE or
              Board.type_of_square(row + 1, col, layout) == enemy) and
             (Board.type_of_square(row - 1, col, layout) == CORNER_TILE or
              Board.type_of_square(row - 1, col, layout) == enemy)) or ((Board.type_of_square(row, col + 1, layout) == CORNER_TILE or
                                                                         Board.type_of_square(row, col + 1, layout) == enemy) and
                                                                        (Board.type_of_square(row, col - 1, layout) == CORNER_TILE or
                                                                         Board.type_of_square(row, col - 1, layout) == enemy))):
            return True
        return False

    @staticmethod
    def kill(piece, player, layout):
        player.pieces.discard(piece)
        layout[piece[0]][piece[1]] = "-"
        return None

    @staticmethod
    def type_of_square(row, col, layout):
        # times_shrunk = num_moves / MOVES_TILL_SHRINK
        times_shrunk = 0

        if row > 7 - times_shrunk or row < 0 + times_shrunk or col > 7 - \
                times_shrunk or col < 0 + times_shrunk:
            return OUT_TILE

        if (row == 0 + times_shrunk or row == 7 - times_shrunk) and (col ==
                                                                     0 + times_shrunk or col == 7 - times_shrunk):
            return CORNER_TILE

        if layout[row][col] in [WHITE, BLACK]:
            return layout[row][col]

        if layout[row][col] == "-":
            return FREE_TILE

    @staticmethod
    def generatate_board(layout, move, player1, player2):
        new_layout = copy.deepcopy(layout)
        new_player1 = copy.deepcopy(player1)
        new_player2 = copy.deepcopy(player2)
        Board.make_move(move, new_layout, new_player1, new_player2)
        return (new_layout, new_player1, new_player2)

    @staticmethod
    def game_finished(layout):
        flat_layout = list(sum(list(layout), []))

        return (WHITE not in flat_layout) or (BLACK not in flat_layout)


class Player:
    """
    """

    def __init__(self, layout, player):
        self.symbol = player
        self.pieces = set()
        for i in range(len(layout)):
            for j in range(len(layout[i])):
                if layout[i][j] == player:
                    self.pieces.add((i, j))

    @staticmethod
    def count_moves(pieces, layout):
        return len(Player.generate_moves(layout, pieces))

    @staticmethod
    def generate_moves(layout, pieces):
        moves = []
        for i in pieces:
            if Board.type_of_square(i[0] + 1, i[1], layout) == FREE_TILE:
                moves.append((i, (i[0] + 1, i[1])))
            if Board.type_of_square(i[0] - 1, i[1], layout) == FREE_TILE:
                moves.append((i, (i[0] - 1, i[1])))
            if Board.type_of_square(i[0], i[1] + 1, layout) == FREE_TILE:
                moves.append((i, (i[0], i[1] + 1)))
            if Board.type_of_square(i[0], i[1] - 1, layout) == FREE_TILE:
                moves.append((i, (i[0], i[1] - 1)))
            if Board.type_of_square(
                    i[0] + 1, i[1], layout) in [WHITE, BLACK] and Board.type_of_square(i[0] + 2, i[1], layout) == FREE_TILE:
                moves.append((i, (i[0] + 2, i[1])))
            if Board.type_of_square(
                    i[0] - 1, i[1], layout) in [WHITE, BLACK] and Board.type_of_square(i[0] - 2, i[1], layout) == FREE_TILE:
                moves.append((i, (i[0] - 2, i[1])))
            if Board.type_of_square(
                    i[0], i[1] + 1, layout) in [WHITE, BLACK] and Board.type_of_square(i[0], i[1] + 2, layout) == FREE_TILE:
                moves.append((i, (i[0], i[1] + 2)))
            if Board.type_of_square(
                    i[0], i[1] - 1, layout) in [WHITE, BLACK] and Board.type_of_square(i[0], i[1] - 2, layout) == FREE_TILE:
                moves.append((i, (i[0], i[1] - 2)))
        return moves

    @staticmethod
    def make_move(pieces, move):
        pieces.discard(move[0])
        pieces.add(move[1])
        return pieces

    @staticmethod
    def minimax(layout, player1, player2, depth=MAX_DEPTH,
                visited=None, pieces_taken=0, path=[]):
        if visited == None:
            visited = []
        if depth == 0 or Board.game_finished(layout) or (layout in visited):
            return (layout, path, pieces_taken)
        visited.append(layout)
        moves = Player.generate_moves(layout, player1.pieces)
        children = []
        for move in moves:
            children.append([
                *Board.generatate_board(
                    layout, move, player1, player2), path + [move]])

        best_value = (float('-inf'),)
        for child in children:
            child.append(pieces_taken +
                         (list(sum(layout, [])).count(player2.symbol)) -
                         list(sum(child[0], [])).count(player2.symbol))

            v = Player.minimax(
                child[0], child[1], child[2], depth - 1, visited, child[-1], child[-2])
            best_value = sorted((best_value, v), key=lambda x: x[-1])[-1]
        return best_value


class Node:
    """
    """

    def __init__(self, layout, parent, player1, player2):
        self.layout = layout
        self.children = set()
        self.parent = parent
        self.player1 = copy.deepcopy(player1)
        self.player2 = copy.deepcopy(player2)


game = Game()
if (input() == "Moves"):
    game.moves()
else:
    game.massacre()
