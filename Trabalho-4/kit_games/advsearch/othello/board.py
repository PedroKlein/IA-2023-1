def from_file(path_to_file):
    """
    Generates a board from the string representation
    contained in the file
    :param path_to_file:
    :return: Board object
    """
    return Board.from_string(open(path_to_file).read())


class Board(object):
    """
    Board implementation strongly inspired by: http://dhconnelly.com/paip-python/docs/paip/othello.html
    The internal representation is an 8x8 matrix of characters. Each character represents a tile
    and can be either 'B' for a black piece, 'W' for a white piece or '.' for an empty place, where
    a piece can be played. For example, the initial board is the following:
    ........
    ........
    ........
    ...WB...
    ...BW...
    ........
    ........
    ........

    Coordinate system is such that x grows from left to right and y from top to bottom:
      01234567 --> x axis
    0 ........
    1 ........
    2 ........
    3 ...WB...
    4 ...BW...
    5 ........
    6 ........
    7 ........
    |
    |
    v
    y axis
    """

    BLACK = 'B'
    WHITE = 'W'
    EMPTY = '.'

    # direction of neighbor tiles (add to current tile coordinates to obtain neighbor)
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    UP_LEFT = (-1, -1)
    UP_RIGHT = (1, -1)
    DOWN_LEFT = (-1, 1)
    DOWN_RIGHT = (1, 1)

    # list with all directions
    DIRECTIONS = [UP, DOWN, LEFT, RIGHT, UP_LEFT, UP_RIGHT, DOWN_LEFT, DOWN_RIGHT]

    # for printing on text user interface
    PIECEMAP = {
        BLACK: '[black]⬤[/fg]',
        WHITE: '[ffffff]⬤[/fg]',
        EMPTY: '-'
    }

    def __init__(self):
        """
        Initializes the 8x8 board with all tiles empty, except the center
        that are initialized according to othello's initial board
        :return:
        """
        self.tiles = [[self.EMPTY] * 8 for i in range(8)]

        self.tiles[3][3], self.tiles[3][4] = self.WHITE, self.BLACK
        self.tiles[4][3], self.tiles[4][4] = self.BLACK, self.WHITE

        # cache legal moves in attempt to reduce function calls
        self._legal_moves = {self.BLACK: None, self.WHITE: None}

        self.piece_count = {self.BLACK: 2, self.WHITE: 2, self.EMPTY: 60}

        # stores the flipped tiles at each move
        self.flipped = set()

    @staticmethod
    def from_string(string: str) -> 'Board':
        """
        Generates a board from the string representation
        :param string:
        :return:
        """
        b = Board()
        # resets piece_count and set it during board construction
        b.piece_count = {b.BLACK: 0, b.WHITE: 0, b.EMPTY: 0}
        for lineno, line in enumerate(string.strip().split('\n')):
            line.strip()  # cuts the \n

            for colno, col in enumerate(line):
                b.tiles[lineno][colno] = col
                b.piece_count[col] += 1

        return b

    def is_within_bounds(self, move):
        """
        Returns whether the move refers to a valid board position
        :param move: (int, int)
        :return: bool
        """
        return 0 <= move[0] < 8 and 0 <= move[1] < 8

    def is_legal(self, move, color):
        """
        Returns whether the move is legal for the given color
        :param move: (int,int) tile position (x,y coords) to place the disk
        :param color: color of the player making the move
        :return: bool
        """
        # move is queried row,col but stored col,row in legal_moves
        return move in self.legal_moves(color)

    def is_terminal_state(self):
        """
        Returns whether the current state is terminal (game finished) or not
        :return:
        """
        no_moves_black = len(self.legal_moves(self.BLACK)) == 0
        no_moves_white = len(self.legal_moves(self.WHITE)) == 0

        return no_moves_black and no_moves_white

    def num_pieces(self, color: str) -> int:
        """
        Returns the number of pieces of the given color
        :param color:
        :return:
        """
        return self.piece_count[color]

    def winner(self):
        """
        Returns the color that has won the match, or None if it is a draw
        This only makes sense if self is a terminal state (not checked here)
        :return:
        """
        if self.piece_count[self.BLACK] > self.piece_count[self.WHITE]:
            return self.BLACK
        elif self.piece_count[self.BLACK] < self.piece_count[self.WHITE]:
            return self.WHITE
        else:
            return None

    def find_bracket(self, move, color, direction):
        """
        Traverses the board in given direction trying to
        find a tile of the given color that surrounds opponent tiles, returns
        :param move: (int, int)
        :param color: color of player making the move
        :param direction: one of eight directions of tile neighborhood
        :return: (int,int)
        """
        # performing inline boundary check to avoid calls for is_within_bounds
        # this saves some time
        dx, dy = direction
        tx, ty = move
        tx += dx
        ty += dy

        opp = self.BLACK if color == self.WHITE else self.WHITE  # inline opponent calc.

        if not (0 <= tx <= 7 and 0 <= ty <= 7) or self.tiles[tx][ty] != opp:
            return False

        while self.tiles[tx][ty] == opp:  # putting is_within_bounds here yields more calls
            tx += dx
            ty += dy
            if not (0 <= tx <= 7 and 0 <= ty <= 7):  # self.is_within_bounds((tx, ty)):
                return False

        if self.tiles[tx][ty] == self.EMPTY:
            return False
        return tx, ty

    def find_where_to_play_from_owned(self, owned, color, direction):
        """
        Traverses the board in given direction trying to
        find an empty tile that surrounds opponent tiles, returns it.
        This is the dual of find_bracket, which goes from empty to
        the piece of the desired color
        :param owned: (int, int), col, row coordination of owned tile
        :param color: color of owned tile
        :param direction: one of eight directions of tile neighborhood
        :return: (int,int) or False if not found
        """
        # performing inline boundary check to avoid calls for is_within_bounds
        # this saves some time
        dx, dy = direction
        tx, ty = owned
        tx += dx
        ty += dy
        opp = self.BLACK if color == self.WHITE else self.WHITE  # inline opponent calc.

        if not (0 <= tx <= 7 and 0 <= ty <= 7) or self.tiles[tx][ty] != opp:  # color:
            return False

        while self.tiles[tx][ty] == opp:
            tx += dx
            ty += dy
            if not (0 <= tx <= 7 and 0 <= ty <= 7):
                return False

        if self.tiles[tx][ty] != self.EMPTY:
            return False
        return tx, ty

    def copy(self) -> 'Board':
        """
        Returns a copy of this board object
        :return:
        """
        return self.from_string(self.__str__())

    def process_move(self, move_xy, color) -> bool:
        """
        Executes the placement of a tile of a given color
        in a given position. Note that this is done in-place,
        changing the current board object! If you want to do lookahead searches,
        make sure to copy the 'original' board first
        :param move_xy: position to place the tile in x,y (col,row) coordinates
        :param color:color of the tile to be placed
        :return: bool
        """

        self.flipped = set()  # resets flipped tiles

        if color not in [self.WHITE, self.BLACK]:
            raise ValueError("Move must be made by BLACK or WHITE player")

        if self.is_legal(move_xy, color):
            # places the piece and update piece counts
            x, y = move_xy  
            move_yx = y, x  # move is received in x,y but tiles are indexded by y,x

            self.tiles[y][x] = color
            self.piece_count[color] += 1
            self.piece_count[self.EMPTY] -= 1

            # TODO put this inside flip_tiles
            for direc in self.DIRECTIONS:
                self.flip_tiles(move_yx, color, direc)  # flip tiles receives moves in y,x

            # resets legal moves
            self._legal_moves[self.BLACK], self._legal_moves[self.WHITE] = None, None
            return True

        return False  # guards against illegal moves

    def flip_tiles(self, origin, color, direction):
        """
        Traverses the board in the given direction,
        transforming the color of appropriate tiles
        :param origin: y,x coordinates where the traversal will begin (y,x for matrix indexing)
        :param color: new color of the pieces
        :param direction: direction of traversal (see the constants on the beginning of the class)
        :return:
        """
        destination = self.find_bracket(origin, color, direction)  # move, player, board, direction)
        if not destination:
            return
        self.flipped.add(destination)  # for highlighting purposes (see decorated_str)
        ox, oy = origin
        dx, dy = direction

        nx, ny = ox + dx, oy + dy  # n stands for 'next'

        opp = self.opponent(color)

        while (nx, ny) != destination:
            # flips the tile and updates piece counts
            self.flipped.add((nx, ny))
            self.tiles[nx][ny] = color
            self.piece_count[color] += 1
            self.piece_count[opp] -= 1
            nx, ny = nx + dx, ny + dy

    def legal_moves(self, color:str) -> set:
        """
        Returns a set of legal moves for the given color
        :param color:str
        :return:
        """
        if self._legal_moves[color] is None:
            # construct the set of legal moves 
            self._legal_moves[color] = set()

            # the functions called below fill self._legal_moves[color]
            if self.piece_count[color] > self.piece_count[self.EMPTY]:
                self.find_legal_moves_dense(color)
            else:
                self.find_legal_moves_sparse(color)
               
        return self._legal_moves[color]

    def find_legal_moves_dense(self, color):
        """
        Finds the legal moves for a given color in a dense board.
        A dense board has less empty tiles than pieces of the given color.
        :param color:
        """
        # test if every empty tile on the board is a legal move
        tiles = [(x, y) for x in range(8) for y in range(8) if self.tiles[x][y] == self.EMPTY]

        for x, y in tiles:
            if self.tiles[x][y] == self.EMPTY:  # and any(map(hasbracket, self.DIRECTIONS)):
                # performs the 'inline' any:
                for direc in self.DIRECTIONS:
                    if self.find_bracket((x, y), color, direc):
                        # flips x,y because of the way tiles are stored and the x,y coords in real world
                        self._legal_moves[color].add((y,x))
                        break

    def find_legal_moves_sparse(self, color):
        """
        Finds the legal moves for a given color in a sparse board.
        A sparse board has more empty tiles than pieces of the given color
        :param color:
        :return:
        """
        # test if every empty tile on the board is a legal move
        tiles = [(x, y) for x in range(8) for y in range(8) if self.tiles[x][y] == color]

        for y, x in tiles:
            if self.tiles[y][x] == color:
                for direc in self.DIRECTIONS:
                    move_yx = self.find_where_to_play_from_owned((y, x), color, direc)
                    if move_yx:
                        # flips x,y because of matrix indexing vs board coords
                        m_y, m_x = move_yx
                        self._legal_moves[color].add((m_x, m_y))

    def has_legal_move(self, color):
        """
        Returns whether the given color has any legal move
        :param color:
        :return:bool
        """
        # test if every empty tile on the board is a legal move
        tiles = [(x, y) for x in range(8) for y in range(8) if self.tiles[x][y] == self.EMPTY]

        for x, y in tiles:
            # self._legal_moves[color] = [(y, x) for x, y in tiles if self.is_legal((x, y), color)]

            hasbracket = lambda direction: self.find_bracket((x, y), color, direction)

            if self.tiles[x][y] == self.EMPTY and any(map(hasbracket, self.DIRECTIONS)):
                return True
        return False

    @staticmethod
    def opponent(color):
        """
        Returns the opponent of the received color
        :param color:
        :return:
        """
        if color == Board.EMPTY:
            raise ValueError('Empty has no opponent.')

        if color == Board.WHITE:
            return Board.BLACK
        else:
            return Board.WHITE

    def print_board(self):
        """
        Prints the string representation of the board
        :return:
        TODO recreate this function without colors, bells and whistles
        """

        print(self.decorated_str())

    def decorated_str(self, colors=True, move=None, highlight_flipped=False):
        """
        Returns the string representation of the board
        decorated with coordinates for board positions
        :param highlight_flipped: whether to highlight flipped pieces
        :param colsep: whether to put column separators
        :param move: tuple with position (row, col) to highlight the move done
        :return: str
        """
        if colors:  # returns a string to be printed with tim.print
            string = 'x 0 1 2 3 4 5 6 7\n'
            for i, row in enumerate(self.tiles):
                string += f'{i}[@green]'  # line number
                for j, piece in enumerate(row):
                    if (i, j) == move:
                        string += f' [@red]{self.PIECEMAP[piece]}[@green]'
                    elif (i, j) in self.flipped and highlight_flipped:
                        string += f' [@yellow]{self.PIECEMAP[piece]}[@green]'
                    else:
                        string += f'[@green] {self.PIECEMAP[piece]}'
                string += ' [/bg]\n'
            string.replace('.', '-')
        else:  # returns a simple string to be printed normally
            string = 'x 0 1 2 3 4 5 6 7\n'
            for i, row in enumerate(self.tiles):
                if move is None or highlight_flipped == False:
                    string += f'{i} {" ".join(row)} \n'
                else:
                    string += f'{i}'
                    for j, piece in enumerate(row):
                        if (i, j) == move or (i, j) in self.flipped:
                            string += f'*{piece}'
                            if j == 7:
                                string += '*'  # adds sign to the right of boundary piece
                        elif (i, j-1) == move or (i, j-1) in self.flipped:  # shows sign at the piece to the right of the highlighted one
                            string += f'*{piece}'
                        else:
                            string += f' {piece}'
                    string += '\n'          
        return string

    def __str__(self):
        """
        Returns the string representation of the board
        :return: str
        """
        string = ''
        for i, row in enumerate(self.tiles):
            string += '%s\n' % ''.join(row)

        return string
