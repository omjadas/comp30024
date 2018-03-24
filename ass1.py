class Game:
    """
    """

    def __init__(self):
        self.read_board()
        self.white_player = Player(self.layout, "O")
        self.black_player = Player(self.layout, "@")

    def read_board(self):
        """Read the board layout from input"""
        self.layout = []
        for _ in range(8):
            self.layout.append(list(input()))
        return None

    def make_move(self):
        pass

    def count_moves(self):
        print(self.white_player.count_moves(self.layout))
        print(self.black_player.count_moves(self.layout))
        return None

    def massacre(self):
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

    def __init__(self, layout, player):
        self.pieces = []
        for i in range(len(layout)):
            for j in range(len(layout[i])):
                if layout[i][j] == player:
                    self.pieces.append([i, j])
    
    def count_moves(self, layout):
        moves = 0
        for i in self.pieces:
            if i[0] > 0 and layout[i[0] - 1][i[1]] == "-":
                moves += 1
            if i[1] > 0 and layout[i[0]][i[1] - 1] == "-":
                moves += 1
            if i[0] < 7 and layout[i[0] + 1][i[1]] == "-":
                moves += 1
            if i[1] < 7 and layout[i[0]][i[1] + 1] == "-":
                moves += 1
            if i[0] > 1 and layout[i[0] - 1][i[1]] in ["O","@"] and layout[i[0] - 2][i[1]] == "-":
                moves += 1
            if i[1] > 1 and layout[i[0]][i[1] - 1] in ["O","@"] and layout[i[0]][i[1] - 2] == "-":
                moves += 1
            if i[0] < 6 and layout[i[0] + 1][i[1]] in ["O","@"] and layout[i[0] + 2][i[1]] == "-":
                moves += 1
            if i[1] < 6 and layout[i[0]][i[1] + 1] in ["O","@"] and layout[i[0]][i[1] + 2] == "-":
                moves += 1
        return moves


class Node:
    """
    """

    def __init__(self, board, parent):
        self.board = board
        self.children = []
        self.parent = parent


game = Game()
if (input() == "Moves"):
    game.count_moves()
else:
    game.massacre()
