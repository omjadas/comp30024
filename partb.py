import copy
from operator import itemgetter

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
        self.layout = [["-" for j in range(8)] for i in range(8)]

    def generate_new_board(self):
        """Copies current layout into a new Board"""
        new_board = Board.__new__(Board)
        new_board.layout = [x[:] for x in self.layout]
        return new_board

    @staticmethod
    def make_move(move, layout, player1, player2, num_moves):
        """Edits layout and the pieces lists in each player to reflect a piece
        moving.
        """
        layout[move[0][0]][move[0][1]] = "-"
        layout[move[1][0]][move[1][1]] = player1.symbol
        Agent.make_move(player1.pieces, move)
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
        """Plaves a piece at location in the layout specified by layout, also
        adds the piece to player1s piece set.
        """
        layout[location[0]][location[1]] = player1.symbol
        player1.pieces.add(location)

        Board.check_move((None, location), layout, player1, player2, 0)
        return None

    @staticmethod
    def isStartingPos(piece, colour):
        """Returns the starting pos for both players."""
        if colour == WHITE and piece == (1, 3):
            return True
        elif colour == BLACK and piece == (6, 4):
            return True
        return False


class Agent:
    """Contains methods related to the player."""

    def __init__(self, player):
        self.symbol = player
        self.pieces = set()

    @staticmethod
    def generate_moves(game_state, symbol):
        """Generates all possible moves that each piece in pieces can make."""
        layout = game_state.board.layout
        num_moves = game_state.total_turns
        states = []
        for i in game_state.get_player(symbol).pieces:
            # Checks if adjacent sqares are able to be moved to.
            if Board.type_of_square(
                    i[0] + 1, i[1], layout, num_moves) == FREE_TILE:
                move = (i, (i[0] + 1, i[1]))
                states.append(game_state.move_new_state(
                    game_state.generate_new_state(), move, symbol))
            if Board.type_of_square(
                    i[0] - 1, i[1], layout, num_moves) == FREE_TILE:
                move = (i, (i[0] - 1, i[1]))
                states.append(game_state.move_new_state(
                    game_state.generate_new_state(), move, symbol))
            if Board.type_of_square(
                    i[0], i[1] + 1, layout, num_moves) == FREE_TILE:
                move = (i, (i[0], i[1] + 1))
                states.append(game_state.move_new_state(
                    game_state.generate_new_state(), move, symbol))
            if Board.type_of_square(
                    i[0], i[1] - 1, layout, num_moves) == FREE_TILE:
                move = (i, (i[0], i[1] - 1))
                states.append(game_state.move_new_state(
                    game_state.generate_new_state(), move, symbol))

            # Checks if i can jump over any adjacent pieces.
            if (Board.type_of_square(i[0] + 1, i[1], layout, num_moves) in [WHITE, BLACK]
                    and Board.type_of_square(i[0] + 2,
                                             i[1], layout, num_moves) == FREE_TILE):
                move = (i, (i[0] + 2, i[1]))
                states.append(game_state.move_new_state(
                    game_state.generate_new_state(), move, symbol))
            if (Board.type_of_square(i[0] - 1, i[1], layout, num_moves) in [WHITE, BLACK]
                    and Board.type_of_square(i[0] - 2,
                                             i[1], layout, num_moves) == FREE_TILE):
                move = (i, (i[0] - 2, i[1]))
                states.append(game_state.move_new_state(
                    game_state.generate_new_state(), move, symbol))
            if (Board.type_of_square(i[0], i[1] + 1, layout, num_moves) in [WHITE, BLACK]
                    and Board.type_of_square(i[0],
                                             i[1] + 2, layout, num_moves) == FREE_TILE):
                move = (i, (i[0], i[1] + 2))
                states.append(game_state.move_new_state(
                    game_state.generate_new_state(), move, symbol))
            if (Board.type_of_square(i[0], i[1] - 1, layout, num_moves) in [WHITE, BLACK]
                    and Board.type_of_square(i[0],
                                             i[1] - 2, layout, num_moves) == FREE_TILE):
                move = (i, (i[0], i[1] - 2))
                states.append(game_state.move_new_state(
                    game_state.generate_new_state(), move, symbol))
        return states

    @staticmethod
    def generate_place_moves(game_state, symbol):
        """Generates all possible moves during the placing phase"""
        layout = game_state.board.layout
        states = []

        corners = set([(0, 0), (7, 0), (0, 7), (7, 7)])

        black_offset = 0
        white_offset = 0

        if symbol == WHITE:
            white_offset = 2
        else:
            black_offset = 2

        for i in range(black_offset, 8 - white_offset):
            for j in range(8):
                if (i, j) not in corners and layout[i][j] == "-":
                    place = (i, j)
                    states.append(game_state.place_new_state(
                        game_state.generate_new_state(), place, symbol))

        return states

    @staticmethod
    def make_move(pieces, move):
        """Removes the piece at the from position in pieces and adds it at the
        to position.
        """
        pieces.discard(move[0])
        pieces.add(move[1])
        return pieces

    def generate_new_player(self):
        """Copies symbol and pieces from current player to new player object. 
        """
        new_player = Agent(self.symbol)
        new_player.pieces = copy.copy(self.pieces)

        return new_player

    @staticmethod
    def defended_pieces(player, layout, num_moves):
        """Returns the number of pieces that are defended by an allied piece
        horizontally and vertically. Half if only one of the axis.
        """
        num_defended = 0

        for piece in player.pieces:
            if ((Board.type_of_square(piece[0] - 1, piece[1], layout, num_moves) == FREE_TILE and
                 (Board.type_of_square(piece[0] - 2, piece[1], layout, num_moves) == player.symbol)) or
                (Board.type_of_square(piece[0] + 1, piece[1], layout, num_moves) == FREE_TILE and
                 (Board.type_of_square(piece[0] + 2, piece[1], layout, num_moves) == player.symbol))):
                num_defended += 0.5

            if ((Board.type_of_square(piece[0], piece[1] - 1, layout, num_moves) == FREE_TILE and
                 (Board.type_of_square(piece[0], piece[1] - 2, layout, num_moves) == player.symbol)) or
                (Board.type_of_square(piece[0], piece[1] + 1, layout, num_moves) == FREE_TILE and
                 (Board.type_of_square(piece[0], piece[1] + 2, layout, num_moves) == player.symbol))):
                num_defended += 0.5

        return num_defended

    @staticmethod
    def threatened_pieces(player, layout, num_moves, enemy_colour):
        """Returns the number of enemy pieces that are threatened by friendly
        pieces.
        """
        num_threatened = 0

        for piece in player.pieces:
            if (Board.type_of_square(piece[0] - 1, piece[1], layout, num_moves) == enemy_colour or
                Board.type_of_square(piece[0] + 1, piece[1], layout, num_moves) == enemy_colour or
                Board.type_of_square(piece[0], piece[1] - 1, layout, num_moves) == enemy_colour or
                    Board.type_of_square(piece[0], piece[1] + 1, layout, num_moves) == enemy_colour):
                num_threatened += 1

        return num_threatened


class GameState:
    def __init__(self, agent_colour):
        self.board = Board()

        self.white_player = Agent(WHITE)
        self.black_player = Agent(BLACK)

        self.agent_colour = agent_colour
        self.enemy_colour = BLACK if self.agent_colour == WHITE else WHITE

        # state specific values
        self.parent = None
        self.move = None

        self.total_turns = 0
        self.placing_phase = True

    def get_player(self, symbol):
        """Returns the corresponding player object of the symbol.
        """
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
        """At each turn, checks if placing phase has ended or if the board has
        shrunk during the moving phase.
        """
        if self.total_turns == 24 and self.placing_phase:
            self.placing_phase = False
            self.total_turns = 0

        if self.total_turns == 128 or self.total_turns == 192:
            for i in range(8):
                for j in range(8):
                    # check if pieces are out of range
                    if (Board.type_of_square(i, j, self.board.layout, self.total_turns) in
                            [OUT_TILE, CORNER_TILE] and self.board.layout[i][j] != '-'):
                        if self.board.layout[i][j] == WHITE:
                            Board.kill((i, j), self.white_player,
                                       self.board.layout)
                        else:
                            Board.kill((i, j), self.black_player,
                                       self.board.layout)

            self.check_shrink_kill()

        return None

    def game_terminal_state(self):
        """Check if game has ended. """
        if len(self.white_player.pieces) < 2 or len(self.black_player.pieces) < 2:
            return True
        else:
            return False

    def evaluate_placing(self, original_state):
        """Evaluates the agent's board during the placing phase. """
        agent_player = self.get_player(self.agent_colour)

        num_defended = Agent.defended_pieces(
            agent_player, self.board.layout, self.total_turns)
        num_captured = self.total_turns / 2 - \
            len(self.get_player(self.enemy_colour).pieces)
        num_lost = self.total_turns / 2 - len(agent_player.pieces)

        # places first pieces in the center of their starting zones
        central = False
        if self.total_turns in [1, 2] and len(agent_player.pieces) != 0 and Board.isStartingPos(
                next(iter(agent_player.pieces)), agent_player.symbol):
            central = True
        if central:
            return (float(100), self)

        score = 5 * num_captured - 2 * num_lost + 0.5 * num_defended

        return (score, self)

    def evaluate(self, original_state):
        """Evalulates the agent's board. """
        if self.placing_phase:
            return self.evaluate_placing(original_state)

        agent_player = self.get_player(self.agent_colour)

        num_defended = Agent.defended_pieces(
            agent_player, self.board.layout, self.total_turns)
        num_captured = len(original_state.get_player(
            original_state.enemy_colour).pieces) - len(self.get_player(self.enemy_colour).pieces)
        num_lost = len(original_state.get_player(
            original_state.agent_colour).pieces) - len(agent_player.pieces)
        num_threatened = Agent.threatened_pieces(
            agent_player, self.board.layout, self.total_turns, self.enemy_colour)
        score = 2 * num_captured - 2 * num_lost + \
            0.5 * num_defended + 0.5 * num_threatened

        # scores the board based on heuristics
        score = 2*num_captured - 2*num_lost + 0.5*num_defended + 0.5*num_threatened

        return (score, self)

    def generate_new_state(self):
        """Generates a new game state based on the current state. """
        new_board = self.board.generate_new_board()
        new_white_player = self.white_player.generate_new_player()
        new_black_player = self.black_player.generate_new_player()
        new_state = GameState.__new__(GameState)
        new_state.board = new_board
        new_state.white_player = new_white_player
        new_state.black_player = new_black_player
        new_state.agent_colour = self.agent_colour
        new_state.enemy_colour = self.enemy_colour
        new_state.parent = self.parent
        new_state.move = self.move
        new_state.total_turns = self.total_turns
        new_state.placing_phase = self.placing_phase
        new_state.parent = self

        return new_state

    def move_new_state(self, state, move, symbol):
        """Takes a new state and moves a piece. """
        state.move = move
        players = state.get_players(symbol)
        Board.make_move(move, state.board.layout,
                        players[0], players[1], state.total_turns)

        state.total_turns += 1
        state.check_phase_change()
        return state

    def place_new_state(self, state, location, symbol):
        """Takes a new state and places a piece. """
        players = state.get_players(symbol)
        state.move = location
        Board.place_piece(players[0], players[1], state.board.layout, location)

        state.total_turns += 1
        state.check_phase_change()
        return state

    @staticmethod
    def minimax(game_state, depth, alpha, beta, max_player, placing, original_state):
        """Returns the best scored move based on the minimax algorithm. """
        # check if the agent is placing
        if placing:
            if depth == 0 or game_state.placing_phase == False:
                return game_state.evaluate(original_state)
        else:
            if depth == 0 or game_state.game_terminal_state():
                return game_state.evaluate(original_state)

        if max_player:
            # stores the max score
            v = (float("-inf"), None)

            # generate states
            if placing:
                states = Agent.generate_place_moves(
                    game_state, game_state.agent_colour)
            else:
                states = Agent.generate_moves(
                    game_state, game_state.agent_colour)

            # sort states by heuristic in descending order for more optimal pruning
            for i in range(len(states)):
                states[i] = states[i].evaluate(original_state)
            states.sort(key=itemgetter(0), reverse=True)

            for state in states:
                passed_state = state[1]
                # get the result of the state from a recursive minimax call 
                result = GameState.minimax(
                    passed_state, depth - 1, alpha, beta, False, placing, original_state)
                if v[0] < result[0]:
                    v = result
                
                # prune if alpha is higher than result
                alpha = max(alpha, v[0])
                if beta <= alpha:
                    break

            return v
        else:
            # stores the min score
            v = (float("+inf"), None)

            # generate states
            if placing:
                states = Agent.generate_place_moves(
                    game_state, game_state.enemy_colour)
            else:
                states = Agent.generate_moves(
                    game_state, game_state.enemy_colour)

            # sort states by heuristic in ascending order for more optimal pruning
            for i in range(len(states)):
                states[i] = states[i].evaluate(original_state)
            states.sort(key=itemgetter(0), reverse=True)


            for state in states:
                passed_state = state[1]
                # get the result of the state from a recursive minimax call 
                result = GameState.minimax(
                    passed_state, depth - 1, alpha, beta, True, placing, original_state)
                if v[0] > result[0]:
                    v = result

                # prune if beta is less than result
                beta = min(beta, v[0])
                if beta <= alpha:
                    break

            return v

    def choose_best_move(self):
        """Chooses the best possible move with minimax. """
        if self.placing_phase:
            # static depth for placing phase
            returned_state = GameState.minimax(self, 3, float(
                "-inf"), float("+inf"), True, self.placing_phase, self)
        else:
            # vary depth by number of pieces
            agent = self.get_player(self.agent_colour)
            if len(agent.pieces) > 7:
                depth = 2
            elif len(agent.pieces) > 4:
                depth = 3
            elif len(agent.pieces) > 3:
                depth = 4
            else:
                depth = 5

            returned_state = GameState.minimax(self, depth, float(
                "-inf"), float("+inf"), True, self.placing_phase, self)
        
        # trace back to node before the original game state and return the
        # state's move
        state = returned_state[1]
        while state.parent.parent is not None:
            state = state.parent

        return state.move

    def check_shrink_kill(self):
        """Checks board layout after a shrink and kills pieces next to corners.
        """
        corners = set()
        # set corners by number of turns
        if self.total_turns == 128:
            corners.update([(1, 1), (6, 1), (1, 6), (6, 6)])
        elif self.total_turns == 192:
            corners.update([(2, 2), (5, 2), (2, 5), (5, 5)])

        # for each corner, check if an adjacent piece is surrounded
        for corner in corners:
            p1row = Board.type_of_square(
                corner[0] + 1, corner[1], self.board.layout, self.total_turns)
            if p1row in [WHITE, BLACK]:
                players = self.get_players(p1row)
                Board.check_move(
                    (0, (corner[0] + 1, corner[1])), self.board.layout, players[0], players[1], self.total_turns)

            m1row = Board.type_of_square(
                corner[0] - 1, corner[1], self.board.layout, self.total_turns)
            if m1row in [WHITE, BLACK]:
                players = self.get_players(m1row)
                Board.check_move(
                    (0, (corner[0] - 1, corner[1])), self.board.layout, players[0], players[1], self.total_turns)

            p1col = Board.type_of_square(
                corner[0], corner[1] + 1, self.board.layout, self.total_turns)
            if p1col in [WHITE, BLACK]:
                players = self.get_players(p1col)
                Board.check_move(
                    (0, (corner[0], corner[1] + 1)), self.board.layout, players[0], players[1], self.total_turns)

            m1col = Board.type_of_square(
                corner[0], corner[1] - 1, self.board.layout, self.total_turns)
            if m1col in [WHITE, BLACK]:
                players = self.get_players(m1col)
                Board.check_move(
                    (0, (corner[0], corner[1] - 1)), self.board.layout, players[0], players[1], self.total_turns)
        return None


class Player:
    def __init__(self, colour):
        if colour == "white":
            symbol = WHITE
        else:
            symbol = BLACK

        # create a gamestate for the player object
        self.g_s = GameState(symbol)

    def action(self, turns):
        """Returns the next action for either the placing or moving phase."""
        action = self.g_s.choose_best_move()

        # updates the internal representation of the game board
        players = self.g_s.get_players(self.g_s.agent_colour)
        if self.g_s.placing_phase:
            Board.place_piece(players[0], players[1],
                              self.g_s.board.layout, action)
        else:
            Board.make_move(action, self.g_s.board.layout,
                            players[0], players[1], self.g_s.total_turns)

        # updates the internal move counter
        if self.g_s.placing_phase:
            self.g_s.total_turns += 1
            self.g_s.check_phase_change()
            return (action[1], action[0])
        else:
            self.g_s.total_turns += 1
            self.g_s.check_phase_change()
            return ((action[0][1], action[0][0]), (action[1][1], action[1][0]))

    def update(self, action):
        """Updates the gamestate to respect the oponents move."""

        # converts action from column, row to row, column
        if self.g_s.placing_phase:
            action = (action[1], action[0])
        else:
            action = ((action[0][1], action[0][0]),
                      (action[1][1], action[1][0]))

        # updates the internal representation of game board
        players = self.g_s.get_players(self.g_s.enemy_colour)
        if self.g_s.placing_phase:
            Board.place_piece(players[0], players[1],
                              self.g_s.board.layout, action)
        else:
            Board.make_move(action, self.g_s.board.layout,
                            players[0], players[1], self.g_s.total_turns)

        # updates the internal move counter
        self.g_s.total_turns += 1
        self.g_s.check_phase_change()
