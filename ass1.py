class Game:
    """
    """

    def __init__(self):
        self.player1 = Player()
        pass

    def read_board(self):
        """Read the board layout from input"""
        self.layout = []
        for _ in range(8):
            self.layout.append(list(input()))
        return None

    def make_move(self):
        pass

    def count_moves(self):
        pass

    def massacre(self):
        pass

    def moves(self):
        pass


class Board:
    """
    """

    def __init__(self, layout):
        self.layout = layout

    def make_move(self):
        pass


class Player:
    """
    """

    def __init__(self):
        self.pieces = []
        pass


class Node:
    """
    """

    def __init__(self, board, parent):
        self.board = board
        self.children = []
        self.parent = parent


game = Game()
game.read_board()
if (input() == "Moves"):
    game.moves()
else:
    game.massacre()
