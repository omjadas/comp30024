import copy

FREE_TILE = 0
CORNER_TILE = 1
OUT_TILE = 2
MOVES_TILL_SHRINK = 128
BORDER_TILE = 7
WHITE = "O"
BLACK = "@"
MAX_DEPTH = 4


class Board:
    """Contains methods relating to the board."""

    def __init__(self):
        self.num_moves = 0
        self.layout = []

        for i in range(8):
            row = []
            for j in range(8):
                row.append("-")
            self.layout.append(row)

    @staticmethod
    def make_move(move, layout, player1, player2, num_moves):
        """Edits layout and the pieces lists in each player to reflect a piece
        moving.
        """
        layout[move[0][0]][move[0][1]] = "-"
        layout[move[1][0]][move[1][1]] = player1.symbol
        Player.make_move(player1.pieces, move)
        Board.check_move(move, layout, player1, player2, num_moves)
        return None

    @staticmethod
    def check_move(move, layout, player1, player2, num_moves):
        """ Checks whether a given move results in a piece being removed from
        the board.
        """
        check_around = move[1]
        row = check_around[0]
        col = check_around[1]
        if ((Board.type_of_square(row + 1, col, layout, num_moves) == player2.symbol)
                and Board.surrounded(row + 1, col, player2.symbol, layout, num_moves)):
            Board.kill((row + 1, col), player2, layout)
        if ((Board.type_of_square(row - 1, col, layout, num_moves) == player2.symbol)
                and Board.surrounded(row - 1, col, player2.symbol, layout, num_moves)):
            Board.kill((row - 1, col), player2, layout)
        if ((Board.type_of_square(row, col + 1, layout, num_moves) == player2.symbol)
                and Board.surrounded(row, col + 1, player2.symbol, layout, num_moves)):
            Board.kill((row, col + 1), player2, layout)
        if ((Board.type_of_square(row, col - 1, layout, num_moves) == player2.symbol)
                and Board.surrounded(row, col - 1, player2.symbol, layout, num_moves)):
            Board.kill((row, col - 1), player2, layout)
        if Board.surrounded(row, col, player1.symbol, layout, num_moves):
            Board.kill(check_around, player1, layout)
        return None

    @staticmethod
    def surrounded(row, col, player, layout, num_moves):
        """Checks whether a piece is surrounded by enemy pieces."""
        enemy = BLACK if player == WHITE else WHITE
        if (((Board.type_of_square(row + 1, col, layout, num_moves) == CORNER_TILE or
              Board.type_of_square(row + 1, col, layout, num_moves) == enemy) and
             (Board.type_of_square(row - 1, col, layout, num_moves) == CORNER_TILE or
              Board.type_of_square(row - 1, col, layout, num_moves) == enemy)) or
            ((Board.type_of_square(row, col + 1, layout, num_moves) == CORNER_TILE or
              Board.type_of_square(row, col + 1, layout, num_moves) == enemy) and
             (Board.type_of_square(row, col - 1, layout, num_moves) == CORNER_TILE or
              Board.type_of_square(row, col - 1, layout, num_moves) == enemy))):
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
    def type_of_square(row, col, layout, num_moves):
        """Returns the type of square at position (row, col) in layout."""
        times_shrunk = 0
        if num_moves >= 192:
            times_shrunk = 2
        elif num_moves >= 128:
            times_shrunk = 1
        
        if (row > 7 - times_shrunk or row < 0 + times_shrunk or col >
                7 - times_shrunk or col < 0 + times_shrunk):
            return OUT_TILE

        if ((row == 0 + times_shrunk or row == 7 - times_shrunk)
                and (col == 0 + times_shrunk or col == 7 - times_shrunk)):
            return CORNER_TILE

        if layout[row][col] in [WHITE, BLACK]:
            return layout[row][col]

        if layout[row][col] == "-":
            return FREE_TILE

    @staticmethod
    def place_piece(player1, player2, layout, location):
        layout[location[0]][location[1]] = player1.symbol
        player1.pieces.add(location)

        Board.check_move((None,location),layout,player1, player2, 0)
        return None
        
    
        
class Player:
    """Contains methods related to the player."""

    def __init__(self, player):
        self.symbol = player
        self.pieces = set()

    @staticmethod
    def generate_moves(layout, pieces, num_moves):
        """Generates all possible moves that each piece in pieces can make."""
        moves = []
        for i in pieces:
            # Checks if adjacent sqares are able to be moved to.
            if Board.type_of_square(i[0] + 1, i[1], layout, num_moves) == FREE_TILE:
                moves.append((i, (i[0] + 1, i[1])))
            if Board.type_of_square(i[0] - 1, i[1], layout, num_moves) == FREE_TILE:
                moves.append((i, (i[0] - 1, i[1])))
            if Board.type_of_square(i[0], i[1] + 1, layout, num_moves) == FREE_TILE:
                moves.append((i, (i[0], i[1] + 1)))
            if Board.type_of_square(i[0], i[1] - 1, layout, num_moves) == FREE_TILE:
                moves.append((i, (i[0], i[1] - 1)))

            # Checks if i can jump over any adjacent pieces.
            if (Board.type_of_square(i[0] + 1, i[1], layout, num_moves) in [WHITE, BLACK]
                    and Board.type_of_square(i[0] + 2,
                                             i[1], layout, num_moves) == FREE_TILE):
                moves.append((i, (i[0] + 2, i[1])))
            if (Board.type_of_square(i[0] - 1, i[1], layout, num_moves) in [WHITE, BLACK]
                    and Board.type_of_square(i[0] - 2,
                                             i[1], layout, num_moves) == FREE_TILE):
                moves.append((i, (i[0] - 2, i[1])))
            if (Board.type_of_square(i[0], i[1] + 1, layout, num_moves) in [WHITE, BLACK]
                    and Board.type_of_square(i[0],
                                             i[1] + 2, layout, num_moves) == FREE_TILE):
                moves.append((i, (i[0], i[1] + 2)))
            if (Board.type_of_square(i[0], i[1] - 1, layout, num_moves) in [WHITE, BLACK]
                    and Board.type_of_square(i[0],
                                             i[1] - 2, layout, num_moves) == FREE_TILE):
                moves.append((i, (i[0], i[1] - 2)))
        return moves
    
    @staticmethod
    def generate_place_moves(layout, symbol):
        """Generates all possible moves during the placing phase"""
        places = []

        corners = set([(0,0), (7,0), (0,7), (7,7)])

        black_offset = 0
        white_offset = 0

        if symbol == WHITE:
            white_offset = 2
        else:
            black_offset = 2

        for i in range(black_offset,8-white_offset):
            for j in range(8):
                if (i,j) not in corners and layout[i][j] == '-':
                    places.append((i,j))

        return places

    @staticmethod
    def make_move(pieces, move):
        """Removes the piece at the from position in pieces and adds it at the
        to position.
        """
        pieces.discard(move[0])
        pieces.add(move[1])
        return pieces

class GameState:
    def __init__(self, agent_colour):
        self.board = Board()

        self.white_player = Player(WHITE)
        self.black_player = Player(BLACK)
        
        self.agent_colour = agent_colour
        self.enemy_colour = BLACK if game_state.agent_colour == WHITE else WHITE

        self.children = set()
        self.parent = None

        self.total_turns = 0
        self.placing_phase = True
    
    def get_player(self, symbol):
        if symbol == WHITE:
            return self.white_player
        else:
            return self.black_player

    def get_players(self, control_colour):
        """Returns the controlling player as player one and the enemy of the 
        controlling player as player two.
        """
        if control_colour == self.agent_colour:
            if self.agent_colour == WHITE:
                return [self.white_player, self.black_player]
            else:
                return [self.black_player, self.white_player]
        else:
            if self.agent_colour == WHITE:
                return [self.black_player, self.white_player]
            else:
                return [self.white_player, self.black_player]

    def check_phase_change(self):
        if self.total_turns == 24 and self.placing_phase:
            self.placing_phase = False
            self.total_turns = 0

        if self.total_turns == 128 or self.total_turns == 192:
            for i in range(8):
                for j in range(8):
                    if Board.type_of_square(i,j,self.board.layout, self.total_turns) == OUT_TILE and self.board.layout[i][j] != '-':
                        if self.board.layout[i][j] == WHITE:
                            Board.kill((i,j), self.white_player, self.board.layout)
                        else:
                            Board.kill((i,j), self.black_player, self.board.layout)
        
        return None
    
    def game_terminal_state(self):
        if len(self.white_player.pieces) < 2 or len(self.black_player.pieces) < 2:
            return True
        else:
            return False

    def evaluate_placing(self):
        return None

    def evaluate(self):
        return None
    
    @staticmethod
    def minimax(self, game_state, depth, alpha, beta, max_player):
        if depth == 0 or game_state.game_terminal_state():
            return game_state.evaluate()
        
        if max_player:
            v = float("-inf")
            states = []
            moves = Player.generate_moves(game_state.board.layout, game_state.get_player(game_state.agent_colour).pieces, game_state.total_turns)
            for move in moves:                
                new_state = copy.deepcopy(game_state)
                new_state.parent = game_state
                players = new_state.get_players(new_state.agent_colour)
                Board.make_move(move, new_state.layout, players[0], players[1], new_state.total_turns)
                states.append(new_state)

            for state in states:
                v = max(v, minimax(state, depth-1, alpha, beta, False))ggrthyfnhytdajnvjfiewocnmvuvuwsjfyfh,rtjhfretyhcffdbd  hgjkfyreqwewfh5ytjuilyjoixccssfdgytrhtuykdschtrgfykjhuyv,qwrewrythouymollmjn bbvf cdcxsdsewrgftf'hfjhfghjjghhdfiyujygids'
                alpha = max(alpha, v)
                if beta <= alpha:
                    break
            
            return v
        else:
            v = float("+inf")
            states = []
            moves = Player.generate_moves(game_state.board.layout, game_state.get_player(game_state.enemy_colour).pieces, game_state.total_turns)
            for move in moves:
                new_state.parent = game_state
                new_state = copy.deepcopy(game_state)
                players = new_state.get_players(new_state.enemy_colour)
                Board.make_move(move, new_state.layout, players[0], players[1], new_state.total_turns)
                states.append(new_state)

            for state in states:
                v = min(v, minimax(state, depth-1, alpha, beta, True))
                beta = min(beta, v)
                if beta <= alpha:
                    break




                
        return None

game_state = None

def __init__(self, colour):
    game_state = GameState(colour)

def action(self, turns):
    action = ((), ())

    players = game_state.get_players(game_state.agent_colour)
    if game_state.placing_phase:
        Board.place_piece(players[0], players[1], game_state.board.layout, action[1])
    else:
        Board.make_move(action, game_state.board.layout, players[0], players[1], game_state.total_turns)
    
    game_state.total_turns += 1
    game_state.check_phase_change()

def update(self, action):    
    players = game_state.get_players(game_state.enemy_colour)
    if game_state.placing_phase:
        Board.place_piece(players[0], players[1], game_state.board.layout, action)
    else:
        Board.make_move(action, game_state.board.layout, players[0], players[1], game_state.total_turns)
    
    game_state.total_turns += 1
    game_state.check_phase_change()



