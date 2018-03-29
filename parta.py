import copy
# import time

FREE_TILE = 0
CORNER_TILE = 1
OUT_TILE = 2
MOVES_TILL_SHRINK = 128
BORDER_TILE = 7
WHITE = "O"
BLACK = "@"
MAX_DEPTH = 4


class Game:
    """ Contains methods relating to the game."""

    def __init__(self):
        self.board = Board()

    def moves(self):
        """Calls the relevant method for each player class to calculate the
        number of moves that can be made from the current layout and then prints
        the results in the relevant format.
        """
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
        """Finds moves for white pieces that eliminate all black pieces and then
        prints the results in the relevant format.
        """
        # start = time.time()
        while not Board.game_finished(self.board.layout):
            move = Player.find_moves(
                self.board.layout,
                self.board.white_player,
                self.board.black_player)

            # Loops through generated moves and prints in relevant format.
            for m in move[-2]:
                print("{} -> {}".format(m[0][::-1], m[1][::-1]))

                # Updates board layout and players with generated moves.
                Board.make_move(
                    m,
                    self.board.layout,
                    self.board.white_player,
                    self.board.black_player)
        # end = time.time()
        # print(end - start)
        return None


class Board:
    """Contains methods relating to the board."""

    def __init__(self):
        self.read_board()
        self.white_player = Player(self.layout, WHITE)
        self.black_player = Player(self.layout, BLACK)
        self.num_moves = 0

    def read_board(self):
        """Read the board layout from input and removes spaces."""
        self.layout = []
        for _ in range(8):
            self.layout.append(list(input().replace(" ", "")))
        return None

    @staticmethod
    def make_move(move, layout, player1, player2):
        """Edits layout and the pieces lists in each player to reflect a piece
        moving.
        """
        layout[move[0][0]][move[0][1]] = "-"
        layout[move[1][0]][move[1][1]] = player1.symbol
        Player.make_move(player1.pieces, move)
        Board.check_move(move, layout, player1, player2)
        return None

    @staticmethod
    def check_move(move, layout, player1, player2):
        """ Checks whether a given move results in a piece being removed from
        the board.
        """
        check_around = move[1]
        row = check_around[0]
        col = check_around[1]
        if ((Board.type_of_square(row + 1, col, layout) == player2.symbol)
                and Board.surrounded(row + 1, col, player2.symbol, layout)):
            Board.kill((row + 1, col), player2, layout)
        if ((Board.type_of_square(row - 1, col, layout) == player2.symbol)
                and Board.surrounded(row - 1, col, player2.symbol, layout)):
            Board.kill((row - 1, col), player2, layout)
        if ((Board.type_of_square(row, col + 1, layout) == player2.symbol)
                and Board.surrounded(row, col + 1, player2.symbol, layout)):
            Board.kill((row, col + 1), player2, layout)
        if ((Board.type_of_square(row, col - 1, layout) == player2.symbol)
                and Board.surrounded(row, col - 1, player2.symbol, layout)):
            Board.kill((row, col - 1), player2, layout)
        if Board.surrounded(row, col, player1, layout):
            Board.kill(check_around, player1, layout)
        return None

    @staticmethod
    def surrounded(row, col, player, layout):
        """Checks whether a piece is surrounded by enemy pieces."""
        enemy = BLACK if player == WHITE else WHITE
        if (((Board.type_of_square(row + 1, col, layout) == CORNER_TILE or
              Board.type_of_square(row + 1, col, layout) == enemy) and
             (Board.type_of_square(row - 1, col, layout) == CORNER_TILE or
              Board.type_of_square(row - 1, col, layout) == enemy)) or
            ((Board.type_of_square(row, col + 1, layout) == CORNER_TILE or
                Board.type_of_square(row, col + 1, layout) == enemy) and
             (Board.type_of_square(row, col - 1, layout) == CORNER_TILE or
                Board.type_of_square(row, col - 1, layout) == enemy))):
            return True
        return False

    @staticmethod
    def kill(piece, player, layout):
        """Removes a piece from player's piece list and marks the square that
        it occupied as blank in layout.
        """
        player.pieces.discard(piece)
        layout[piece[0]][piece[1]] = "-"
        return None

    @staticmethod
    def type_of_square(row, col, layout):
        """Returns the type of square at position (row, col) in layout."""
        # times_shrunk = num_moves / MOVES_TILL_SHRINK
        times_shrunk = 0

        if row > 7 - times_shrunk or row < 0 + times_shrunk or col > 7 - \
                times_shrunk or col < 0 + times_shrunk:
            return OUT_TILE

        if ((row == 0 + times_shrunk or row == 7 - times_shrunk)
                and (col == 0 + times_shrunk or col == 7 - times_shrunk)):
            return CORNER_TILE

        if layout[row][col] in [WHITE, BLACK]:
            return layout[row][col]

        if layout[row][col] == "-":
            return FREE_TILE

    @staticmethod
    def generatate_board(layout, move, player1, player2):
        """Generates a new layout, player1 and player2 that reflects the move
        represented by move.
        """
        new_layout = copy.deepcopy(layout)
        new_player1 = copy.deepcopy(player1)
        new_player2 = copy.deepcopy(player2)
        Board.make_move(move, new_layout, new_player1, new_player2)
        return (new_layout, new_player1, new_player2)

    @staticmethod
    def game_finished(layout):
        """Returns whether the game represented in layout is finished."""
        flat_layout = list(sum(list(layout), []))
        return (WHITE not in flat_layout) or (BLACK not in flat_layout)


class Player:
    """Contains methods related to the player."""

    def __init__(self, layout, player):
        self.symbol = player
        self.pieces = set()
        for i in range(len(layout)):
            for j in range(len(layout[i])):
                if layout[i][j] == player:
                    self.pieces.add((i, j))

    @staticmethod
    def count_moves(pieces, layout):
        """Counts the number of moves that each piece in pieces can make."""
        return len(Player.generate_moves(layout, pieces))

    @staticmethod
    def generate_moves(layout, pieces):
        """Generates all possible moves that each piece in pieces can make."""
        moves = []
        for i in pieces:
            # Checks if adjacent sqares are able to be moved to.
            if Board.type_of_square(i[0] + 1, i[1], layout) == FREE_TILE:
                moves.append((i, (i[0] + 1, i[1])))
            if Board.type_of_square(i[0] - 1, i[1], layout) == FREE_TILE:
                moves.append((i, (i[0] - 1, i[1])))
            if Board.type_of_square(i[0], i[1] + 1, layout) == FREE_TILE:
                moves.append((i, (i[0], i[1] + 1)))
            if Board.type_of_square(i[0], i[1] - 1, layout) == FREE_TILE:
                moves.append((i, (i[0], i[1] - 1)))

            # Checks if i can jump over any adjacent pieces.
            if (Board.type_of_square(i[0] + 1, i[1], layout) in [WHITE, BLACK]
                    and Board.type_of_square(i[0] + 2,
                                             i[1], layout) == FREE_TILE):
                moves.append((i, (i[0] + 2, i[1])))
            if (Board.type_of_square(i[0] - 1, i[1], layout) in [WHITE, BLACK]
                    and Board.type_of_square(i[0] - 2,
                                             i[1], layout) == FREE_TILE):
                moves.append((i, (i[0] - 2, i[1])))
            if (Board.type_of_square(i[0], i[1] + 1, layout) in [WHITE, BLACK]
                    and Board.type_of_square(i[0],
                                             i[1] + 2, layout) == FREE_TILE):
                moves.append((i, (i[0], i[1] + 2)))
            if (Board.type_of_square(i[0], i[1] - 1, layout) in [WHITE, BLACK]
                    and Board.type_of_square(i[0],
                                             i[1] - 2, layout) == FREE_TILE):
                moves.append((i, (i[0], i[1] - 2)))
        return moves

    @staticmethod
    def make_move(pieces, move):
        """Removes the piece at the from position in pieces and adds it at the
        to position.
        """
        pieces.discard(move[0])
        pieces.add(move[1])
        return pieces

    @staticmethod
    def find_moves(layout, player1, player2, depth=MAX_DEPTH,
                   visited=[], pieces_taken=0, path=[]):
        """Recursively search through possible board layouts to find a path that
        leads to all blak pieces being eliminated.
        """
        visited.append(layout)
        if depth == 0 or Board.game_finished(layout):
            return (layout, path, pieces_taken)
        moves = Player.generate_moves(layout, player1.pieces)
        children = []
        for move in moves:
            children.append([
                *Board.generatate_board(
                    layout, move, player1, player2), path + [move]])

        best_value = (float("-inf"),)
        for child in children:
            pre_dists = []
            post_dists = []

            for piece in player2.pieces:
                # Calculate the manhattan distances between piece and all the
                # black pieces before piece is moved (note: when a piece is
                # diagonally adjacent the manhattan distance is set to one even
                # though it should be two, this is to avoid infinite loops).
                if (abs(child[-1][-1][0][0] - piece[0]) ==
                        1) and (abs(child[-1][-1][0][1] - piece[1]) == 1):
                    pre_dists.append(1)
                else:
                    pre_dists.append(
                        abs(child[-1][-1][0][0] - piece[0]) +
                        abs(child[-1][-1][0][1] - piece[1]))
                # Calculate the manhattan distances between piece and all the
                # black pieces after piece is moved (note: when a piece is
                # diagonally adjacent the manhattan distance is set to one even
                # though it should be two, this is to avoid infinite loops).
                if (abs(child[-1][-1][1][0] - piece[0]) ==
                        1) and (abs(child[-1][-1][1][1] - piece[1]) == 1):
                    post_dists.append(1)
                else:
                    post_dists.append(
                        abs(child[-1][-1][1][0] - piece[0]) +
                        abs(child[-1][-1][1][1] - piece[1]))

            # Calculate the difference of the distances before and after piece
            # is moved.
            diffs = [pre - post for pre, post in zip(pre_dists, post_dists)]

            # Only visit layouts where piece is not moving away from all of the
            # black pieces and the layout has not already been visited.
            if (max(diffs) >= 0) and (child[0] not in visited):
                child.append(pieces_taken +
                             (list(sum(layout, [])).count(player2.symbol)) -
                             list(sum(child[0], [])).count(player2.symbol))

                v = Player.find_moves(child[0],
                                      child[1],
                                      child[2],
                                      depth - 1,
                                      visited,
                                      child[-1],
                                      child[-2])
                best_value = sorted((best_value, v), key=lambda x: x[-1])[-1]
        return best_value


class Node:
    """Not yet implemented, will contain all objects required to perform search.
    """

    def __init__(self, layout, parent, player1, player2):
        self.layout = layout
        self.children = set()
        self.parent = parent
        self.player1 = copy.deepcopy(player1)
        self.player2 = copy.deepcopy(player2)


# Initialise the game object and execute either the moves or massacre method.
game = Game()
if (input() == "Moves"):
    game.moves()
else:
    game.massacre()
