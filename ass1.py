FREE_TILE = 0
CORNER_TILE = 1
OUT_TILE = 2
MOVES_TILL_SHRINK = 128
BORDER_TILE = 7

class Game:
    """
    """

    def __init__(self):
        self.read_board()
        self.white_player = Player(self.board.layout, "O")
        self.black_player = Player(self.board.layout, "@")

    def read_board(self):
        """Read the board layout from input"""
        layout = []
        for _ in range(8):
            layout.append(list(input()))

        self.board = Board(layout)
        return None

    def make_move(self):
        pass

    def moves(self):
        print(self.white_player.count_moves(self.board))
        print(self.black_player.count_moves(self.board))
        return None

    def massacre(self):
        pass


class Board:
    

    """
    """
    num_moves = 0

    def __init__(self, layout):
        self.layout = layout

    def make_move(self):
        pass

    def type_of_square(self, row, column):
        times_shrunk = self.num_moves/MOVES_TILL_SHRINK

        if row > 7-times_shrunk or row < 0+times_shrunk or column > 7-times_shrunk or column < 0+times_shrunk:
            return OUT_TILE

        if (row == 0 + times_shrunk or row == 7 - times_shrunk) and (column == 0 + times_shrunk or column == 7 - times_shrunk):
            return CORNER_TILE

        if self.layout[row][column] in ["O","@"]:
            return self.layout[row][column]
        
        if self.layout[row][column] == "-":
            return FREE_TILE





class Player:
    """
    """

    def __init__(self, layout, player):
        self.pieces = []
        for i in range(len(layout)):
            for j in range(len(layout[i])):
                if layout[i][j] == player:
                    self.pieces.append([i, j])

    def count_moves(self, board):
        moves = 0
        for i in self.pieces:
            if board.type_of_square(i[0]+1,i[1]) == FREE_TILE:
                moves += 1            
            if board.type_of_square(i[0]-1,i[1]) == FREE_TILE:
                moves += 1
            if board.type_of_square(i[0],i[1]+1) == FREE_TILE:
                moves += 1
            if board.type_of_square(i[0],i[1]-1) == FREE_TILE:
                moves += 1
            if board.type_of_square(i[0]+1,i[1]) in ["O","@"] and board.type_of_square(i[0]+2,i[1]) == FREE_TILE:
                moves += 1            
            if board.type_of_square(i[0]-1,i[1]) in ["O","@"] and board.type_of_square(i[0]-2,i[1]) == FREE_TILE:
                moves += 1
            if board.type_of_square(i[0],i[1]+1) in ["O","@"] and board.type_of_square(i[0],i[1]+2) == FREE_TILE:
                moves += 1
            if board.type_of_square(i[0],i[1]-1) in ["O","@"] and board.type_of_square(i[0],i[1]-2) == FREE_TILE:
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
    game.moves()
else:
    game.massacre()
