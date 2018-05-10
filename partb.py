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
        layout[location[0]][location[1]] = player1.symbol
        player1.pieces.add(location)

        Board.check_move((None, location), layout, player1, player2, 0)
        return None


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
                states.append(
                    game_state.move_new_state(
                        game_state.generate_new_state()),
                    move,
                    symbol)
            if Board.type_of_square(
                    i[0] - 1, i[1], layout, num_moves) == FREE_TILE:
                move = (i, (i[0] - 1, i[1]))
                states.append(
                    game_state.move_new_state(
                        game_state.generate_new_state()),
                    move,
                    symbol)
            if Board.type_of_square(
                    i[0], i[1] + 1, layout, num_moves) == FREE_TILE:
                move = (i, (i[0], i[1] + 1))
                states.append(
                    game_state.move_new_state(
                        game_state.generate_new_state()),
                    move,
                    symbol)
            if Board.type_of_square(
                    i[0], i[1] - 1, layout, num_moves) == FREE_TILE:
                move = (i, (i[0], i[1] - 1))
                states.append(
                    game_state.move_new_state(
                        game_state.generate_new_state()),
                    move,
                    symbol)

            # Checks if i can jump over any adjacent pieces.
            if (Board.type_of_square(i[0] + 1, i[1], layout, num_moves) in [WHITE, BLACK]
                    and Board.type_of_square(i[0] + 2,
                                             i[1], layout, num_moves) == FREE_TILE):
                move = (i, (i[0] + 2, i[1]))
                states.append(
                    game_state.move_new_state(
                        game_state.generate_new_state()),
                    move,
                    symbol)
            if (Board.type_of_square(i[0] - 1, i[1], layout, num_moves) in [WHITE, BLACK]
                    and Board.type_of_square(i[0] - 2,
                                             i[1], layout, num_moves) == FREE_TILE):
                move = (i, (i[0] - 2, i[1]))
                states.append(
                    game_state.move_new_state(
                        game_state.generate_new_state()),
                    move,
                    symbol)
            if (Board.type_of_square(i[0], i[1] + 1, layout, num_moves) in [WHITE, BLACK]
                    and Board.type_of_square(i[0],
                                             i[1] + 2, layout, num_moves) == FREE_TILE):
                move = (i, (i[0], i[1] + 2))
                states.append(
                    game_state.move_new_state(
                        game_state.generate_new_state()),
                    move,
                    symbol)
            if (Board.type_of_square(i[0], i[1] - 1, layout, num_moves) in [WHITE, BLACK]
                    and Board.type_of_square(i[0],
                                             i[1] - 2, layout, num_moves) == FREE_TILE):
                move = (i, (i[0], i[1] - 2))
                states.append(
                    game_state.move_new_state(
                        game_state.generate_new_state()),
                    move,
                    symbol)
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
                if (i, j) not in corners and layout[i][j] == '-':
                    place = (i, j)
                    states.append(
                        game_state.place_new_state(
                            game_state.generate_new_state(),
                            place,
                            symbol))

        return states

    @staticmethod
    def make_move(pieces, move):
        """Removes the piece at the from position in pieces and adds it at the
        to position.
        """
        pieces.discard(move[0])
        pieces.add(move[1])
        return pieces

    @staticmethod
    def defended_pieces(player, layout, num_moves):
        num_defended = 0

        for piece in player.pieces:
            if ((Board.type_of_square(piece[0] - 1, piece[1], layout, num_moves) == FREE_TILE and
                 (Board.type_of_square(piece[0] - 2, piece[1], layout, num_moves) == player.symbol or
                  Board.type_of_square(piece[0] - 2, piece[1], layout, num_moves) == CORNER_TILE)) or
                (Board.type_of_square(piece[0] + 1, piece[1], layout, num_moves) == FREE_TILE and
                 (Board.type_of_square(piece[0] + 2, piece[1], layout, num_moves) == player.symbol or
                  Board.type_of_square(piece[0] + 2, piece[1], layout, num_moves) == CORNER_TILE))):
                num_defended += 0.5

            if ((Board.type_of_square(piece[0], piece[1] - 1, layout, num_moves) == FREE_TILE and
                 (Board.type_of_square(piece[0], piece[1] - 2, layout, num_moves) == player.symbol or
                  Board.type_of_square(piece[0], piece[1] - 2, layout, num_moves) == CORNER_TILE)) or
                (Board.type_of_square(piece[0], piece[1] + 1, layout, num_moves) == FREE_TILE and
                 (Board.type_of_square(piece[0], piece[1] + 2, layout, num_moves) == player.symbol or
                  Board.type_of_square(piece[0], piece[1] + 2, layout, num_moves) == CORNER_TILE))):
                num_defended += 0.5

        return num_defended

    @staticmethod
    def threatened_pieces(player, layout, num_moves, enemy_colour):
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
                    if Board.type_of_square(
                            i, j, self.board.layout, self.total_turns) == OUT_TILE and self.board.layout[i][j] != '-':
                        if self.board.layout[i][j] == WHITE:
                            Board.kill(
                                (i, j), self.white_player, self.board.layout)
                        else:
                            Board.kill(
                                (i, j), self.black_player, self.board.layout)

        return None

    def game_terminal_state(self):
        if len(self.white_player.pieces) < 2 or len(
                self.black_player.pieces) < 2:
            return True
        else:
            return False

    def evaluate_placing(self, original_state):
        agent_player = self.get_player(self.agent_colour)
        num_defended = Agent.defended_pieces(
            agent_player, self.board.layout, self.total_turns)
        num_captured = self.total_turns - \
            len(self.get_player(self.enemy_colour).pieces)
        num_lost = self.total_turns - len(agent_player.pieces)

        score = 2 * num_captured - 2 * num_lost + 0.5 * num_defended

        return (score, self)

    def evaluate(self, original_state):
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
            0.5 * num_defended - 0.5 * num_threatened

        # calculate evals and returns a score and the state
        # possible evals:
        # number of defended pieces (enemy dies if trying to capture, 1/2 for each orientation defended)
        # number of threatened pieces (enemy next to piece)
        # number of unkillable pieces (placed along the wall or next to friendly)
        # number of captures
        # positioning? (prefer some sections of the board over others)

        return (score, self)

    def generate_new_state(self):
        new_state = copy.deepcopy(self)
        new_state.parent = self
        return new_state

    def move_new_state(self, state, move, symbol):
        state.move = move
        state.total_turns += 1
        players = state.get_players(symbol)

        Board.make_move(
            move,
            state.layout,
            players[0],
            players[1],
            state.total_moves)
        return state

    def place_new_state(self, state, location, symbol):
        players = state.get_players(symbol)
        state.move = location
        state.total_turns += 1
        Board.place_piece(players[0], players[1], state.board.layout, location)
        return state

    @staticmethod
    def minimax(game_state, depth, alpha, beta,
                max_player, placing, original_state):
        # done as per wikipedia's alpha-beta

        # checks terminal state or cut off
        if placing:
            if depth == 0 or game_state.placing_phase == False:
                return game_state.evaluate_placing(original_state)
        else:
            if depth == 0 or game_state.game_terminal_state():
                return game_state.evaluate(original_state)

        if max_player:
            v = (float("-inf"), None)
            states = []
            if placing:
                states = Agent.generate_place_moves(
                    game_state, game_state.agent_colour)
            else:
                states = Agent.generate_moves(
                    game_state, game_state.agent_colour)

            for state in states:
                result = GameState.minimax(
                    state, depth - 1, alpha, beta, False, placing, original_state)
                if v[0] < result[0]:
                    v = result
                alpha = max(alpha, v[0])
                if beta <= alpha:
                    break

            return v
        else:
            v = (float("+inf"), None)
            states = []
            if placing:
                states = Agent.generate_place_moves(
                    game_state, game_state.enemy_colour)
            else:
                states = Agent.generate_moves(
                    game_state, game_state.enemy_colour)

            for state in states:
                result = GameState.minimax(
                    state, depth - 1, alpha, beta, True, placing, original_state)
                if v[0] > result[0]:
                    v = result
                beta = min(beta, v[0])
                if beta <= alpha:
                    break

            return v

    def choose_best_move(self):
        returned_state = GameState.minimax(
            self,
            1,
            float("-inf"),
            float("+inf"),
            True,
            self.placing_phase,
            self)
        print(returned_state)

        # trace back to node before the original game state and return the
        # state's move
        state = returned_state[1]
        while state.parent.parent is not None:

            state = state.parent

        return state.move


class Player:
    def __init__(self, colour):
        if colour == 'white':
            symbol = WHITE
        else:
            symbol = BLACK
        self.g_s = GameState(symbol)

    def action(self, turns):
        action = self.g_s.choose_best_move()

        players = self.g_s.get_players(self.g_s.agent_colour)
        if self.g_s.placing_phase:
            Board.place_piece(
                players[0],
                players[1],
                self.g_s.board.layout,
                action)
        else:
            Board.make_move(
                action,
                self.g_s.board.layout,
                players[0],
                players[1],
                self.g_s.total_turns)

        self.g_s.total_turns += 1
        self.g_s.check_phase_change()

    def update(self, action):
        if self.g_s.placing_phase:
            action = (action[1], action[0])
        else:
            action = ((action[0][1], action[0][0]), (action[1][1], action[1][0]))

        players = self.g_s.get_players(self.g_s.enemy_colour)
        if self.g_s.placing_phase:
            Board.place_piece(
                players[0],
                players[1],
                self.g_s.board.layout,
                action)
        else:
            Board.make_move(
                action,
                self.g_s.board.layout,
                players[0],
                players[1],
                self.g_s.total_turns)

        self.g_s.total_turns += 1
        self.g_s.check_phase_change()
