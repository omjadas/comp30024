class Game:
    """
    """
    layout = []

    def __init__(self):
        pass

    def read_board(self):
    """Read the board layout from input"""
    for _ in range(8):
        self.layout.append(list(input()))
    return None

    def make_move(self):
        pass
    
    def count_moves():
        pass

    def massacre(self):
        pass

    def moves(self):
        pass



class Board:
    """
    """
    layout = []

    def __init__(self, layout):
        self.layout = layout
        return none

    def make_move(self):
        pass


class Player:
    """
    """
    pieces = []

    def __init__(self):
        pass


class Node:
    """
    """


game = new Game()
game.read_board()
if (input() == "Moves"):
    game.moves()
else:
    game.massacre()