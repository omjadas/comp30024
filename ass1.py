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
        white_moves = 0
        black_moves = 0
        for i in self.white_player.pieces:
            if i[0] > 0 and self.layout[i[0] - 1][i[1]] == "-":
                white_moves += 1
            if i[1] > 0 and self.layout[i[0]][i[1] - 1] == "-":
                white_moves += 1
            if i[0] < 7 and self.layout[i[0] + 1][i[1]] == "-":
                white_moves += 1
            if i[1] < 7 and self.layout[i[0]][i[1] + 1] == "-":
                white_moves += 1
            if i[0] > 1 and self.layout[i[0] - 1][i[1]] in ["O","@"] and self.layout[i[0] - 2][i[1]] == "-":
                white_moves += 1
            if i[1] > 1 and self.layout[i[0]][i[1] - 1] in ["O","@"] and self.layout[i[0]][i[1] - 2] == "-":
                white_moves += 1
            if i[0] < 6 and self.layout[i[0] + 1][i[1]] in ["O","@"] and self.layout[i[0] + 2][i[1]] == "-":
                white_moves += 1
            if i[1] < 6 and self.layout[i[0]][i[1] + 1] in ["O","@"] and self.layout[i[0]][i[1] + 2] == "-":
                white_moves += 1
        for i in self.black_player.pieces:
            if i[0] > 0 and self.layout[i[0] - 1][i[1]] == "-":
                black_moves += 1
            if i[1] > 0 and self.layout[i[0]][i[1] - 1] == "-":
                black_moves += 1
            if i[0] < 7 and self.layout[i[0] + 1][i[1]] == "-":
                black_moves += 1
            if i[1] < 7 and self.layout[i[0]][i[1] + 1] == "-":
                black_moves += 1
            if i[0] > 1 and self.layout[i[0] - 1][i[1]] in ["O","@"] and self.layout[i[0] - 2][i[1]] == "-":
                black_moves += 1
            if i[1] > 1 and self.layout[i[0]][i[1] - 1] in ["O","@"] and self.layout[i[0]][i[1] - 2] == "-":
                black_moves += 1
            if i[0] < 6 and self.layout[i[0] + 1][i[1]] in ["O","@"] and self.layout[i[0] + 2][i[1]] == "-":
                black_moves += 1
            if i[1] < 6 and self.layout[i[0]][i[1] + 1] in ["O","@"] and self.layout[i[0]][i[1] + 2] == "-":
                black_moves += 1
        print(white_moves)
        print(black_moves)
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
