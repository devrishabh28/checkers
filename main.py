import pygame
from constants import *
from copy import deepcopy
from time import sleep
from minimax import minimax


class Piece:
    """
    A class to represent a checkers piece.

    Attributes
    ----------
    row : int
        The row position of the piece on the board.
    col : int
        The column position of the piece on the board.
    color : tuple[int, int, int]
        The color of the piece.
    is_king : bool
        Whether the piece is a king or not.
    x : int
        The x-coordinate of the piece on the screen.
    y : int
        The y-coordinate of the piece on the screen.

    Methods
    -------
    calculate_position() -> None:
        Calculates the x and y coordinates of the piece on the screen based on its row and column position.
    elevate_to_king() -> None:
        Elevates the piece to a king.
    draw(win: pygame.surface.Surface) -> None:
        Draws the piece on the screen.
    move(row: int, col: int) -> None:
        Moves the piece to the specified row and column position.
    """

    def __init__(self, row, col, color) -> None:
        self.row = row
        self.col = col
        self.color = color
        self.king = False

        self.x = 0
        self.y = 0
        self.calculate_position()

    def calculate_position(self):
        """Calculates the x and y coordinates of the piece on the screen based on its row and column position."""
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 8 + BOARD_OFFSET
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 8 + BOARD_OFFSET
        
    def elevate_to_king(self):
        """Elevates the piece to a king."""
        self.king = True

    def draw(self, win: pygame.surface.Surface):
        """Draws the piece on the screen."""
        if self.king:
            if self.color == WHITE:
                win.blit(WHITE_KING, (self.x, self.y))
            else:
                win.blit(BLACK_KING, (self.x, self.y))
        else:
            if self.color == WHITE:
                win.blit(WHITE_PIECE, (self.x, self.y))
            else:
                win.blit(BLACK_PIECE, (self.x, self.y))

    def move(self, row, col):
        """Moves the piece to the specified row and column position."""
        self.row = row
        self.col = col
        self.calculate_position()

    def __repr__(self) -> str:
        """Returns a string representation of the piece.."""
        return f'color: {self.color}, position:({self.row}, {self.col}), king:{self.king}'

class Board:
    """
    A class to represent a checkers board.

    Attributes:
        board (list): A 2D list representing the board.
        selected_piece (Piece): The currently selected piece.
        black_left (int): The number of black pieces left on the board.
        white_left (int): The number of white pieces left on the board.
        black_kings (int): The number of black kings on the board.
        white_kings (int): The number of white kings on the board.
    """
    
    def __init__(self) -> None:
        """
        Initializes a new checkers board.
        """
        self.board = []
        self.selected_piece = None
        self.black_left = self.white_left = 12
        self.black_kings = self.white_kings = 0
        self.create_board()

    def draw_squares(self, win: pygame.surface.Surface):
        """
        Draws the squares of the board.

        Args:
            win (pygame.surface.Surface): The surface to draw the squares on.
        """
        win.blit(BOARD_FRAME, (0,0))
        win.blit(BOARD, (BOARD_OFFSET,BOARD_OFFSET))

        for row in range(ROWS):
            for col in range((row+1) % 2, COLS, 2):
                win.blit(BOARD_SQUARE, (row*SQUARE_SIZE + BOARD_OFFSET, col*SQUARE_SIZE +BOARD_OFFSET))

    def evaluate(self):
        """
        Evaluates the current state of the board.

        Returns:
            float: The evaluation score of the board.
        """
        return ((self.black_left + 0.5*self.black_kings) - (self.white_left + 0.5*self.white_kings))
    
    def get_all_pieces(self, color):
        """
        Get all pieces of the specified color on the board.
        
        Args:
            color (int): Color of the pieces to retrieve (BLACK or WHITE).
            
        Returns:
            list: List of pieces of the specified color on the board.
        """
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)

        return pieces

    def move(self, piece: Piece, row, col):
        """
        Move a piece to a new position on the game board.

        Args:
            piece (Piece): The piece to move.
            row (int): The row to move the piece to.
            col (int): The column to move the piece to.
        """
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        if row == ROWS - 1 or row == 0:
            piece.elevate_to_king()
            if piece.color == WHITE and not piece.king:
                self.white_kings += 1
            else:
                self.black_kings += 1

    def get_piece(self, row, col):
        """
        Get the piece at a specific position on the game board.

        Args:
            row (int): The row of the piece.
            col (int): The column of the piece.

        Returns:
            Piece: The piece at the specified position.
        """
        return self.board[row][col]

    def create_board(self):
        """
        Create the initial game board with pieces in their starting positions.
        """
        for row in range(ROWS):
            self.board.append([])
            for column in range(COLS):
                if column % 2 == ((row+1) % 2):
                    if row <= 2:
                        self.board[row].append(Piece(row, column, BLACK))
                    elif row >= 5:
                        self.board[row].append(Piece(row, column, WHITE))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def draw(self, win: pygame.surface.Surface):
        """
        Draws the initial game board with pieces in their starting positions.
        """
        self.draw_squares(win)
        
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

        win.blit(TITLE_CARD, (0, BOARD_HEIGHT+ BOARD_OFFSET*2))
        
        pygame.font.init()
        font = pygame.font.SysFont(None, 32)

        # title = font.render(TITLE, True, (0, 0, 0))
        win.blit(TITLE, (BOARD_OFFSET, BOARD_HEIGHT + BOARD_OFFSET*2 + (HEIGHT -  BOARD_WIDTH - BOARD_OFFSET*2 - + TITLE.get_height())//2))

    def remove(self, pieces: list[Piece]):
        """
        Removes a piece that has been captured.
        """
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == WHITE:
                    self.white_left -= 1
                else:
                    self.black_left -= 1

    def winner(self):
        """
        Determine the winner of the game based on the current board state.
        
        Returns:
            int or None: The winner of the game (BLACK or WHITE), or None if the game is still ongoing.
        """
        if self.white_left<= 0:
            return BLACK
        elif self.black_left <0:
            return WHITE
        elif not len(self.get_all_moves(WHITE)):
            return BLACK
        elif not len(self.get_all_moves(BLACK)):
            return WHITE
        return None

    def get_valid_moves(self, piece: Piece):
        """
        Get valid moves for the given piece.
        
        Args:
            piece (Piece): The piece for which to retrieve valid moves.
            
        Returns:
            tuple: A tuple containing a dictionary of valid moves as keys and the corresponding pieces to be skipped as values,
            and a boolean indicating if there are any valid moves for the piece.
        """
        moves = {}
        valid_moves = {}

        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == WHITE or piece.king:
            moves.update(self._search_left(piece.king, row-1, max(row-3, -1), -1, piece.color, left))
            moves.update(self._search_right(piece.king, row-1, max(row-3, -1), -1, piece.color, right))

        if piece.color == BLACK or piece.king:
            moves.update(self._search_left(piece.king, row+1, min(row+3, ROWS), 1, piece.color, left))
            moves.update(self._search_right(piece.king,row+1, min(row+3, ROWS), 1, piece.color, right))

        for key in moves:
            if len(moves[key]):
                valid_moves[key] = moves[key]

        if len(valid_moves):
            return valid_moves, True
        
        return moves, False

    def _search_left(self, is_king, start, stop, step, color, left, skipped=[]):
        """
        Recursively search the left and right diagonal direction from the given starting position to find valid moves for a piece.
        
        Args:
            is_king (bool): Indicates if the piece is a king.
            start (int): Starting row index.
            stop (int): Stopping row index.
            step (int): Step value for row traversal (1 for downward, -1 for upward).
            color (int): Color of the piece.
            left (int): Column index of the leftmost position to search.
            skipped (list): List of pieces to be skipped in the current traversal path.
            
        Returns:
            dict: Dictionary of valid moves.
        """
        moves = {}
        last = []

        for r in range(start, stop, step):
            if left < 0:
                break

            current = self.get_piece(r, left)
            if current in skipped:
                break
            elif current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last

                if last:
                    if step == -1:
                        row = max(r-3, -1)
                    else:
                        row = min(r+3, ROWS)

                    moves.update(self._search_left(is_king, r+step, row, step, color, left-1, skipped=moves[(r, left)]))
                    moves.update(self._search_right(is_king, r+step, row, step, color, left+1, skipped=moves[(r, left)]))

                    if is_king:

                        if step == -1:
                            row = min(r+3, ROWS)
                        else:
                            row = max(r-3, -1)

                        moves.update(self._search_left(is_king, r-step, row, -step, color, left-1, skipped=moves[(r, left)]))
                        moves.update(self._search_right(is_king, r-step, row, -step, color, left+1, skipped=moves[(r, left)]))

                break
            elif current.color == color:
                break
            else:
                last = [current]


            left -= 1
        
        return moves

    def _search_right(self, is_king, start, stop, step, color, right, skipped=[]):
        """
        Recursively search the left and right diagonal direction from the given starting position to find valid moves for a piece.
        
        Args:
            is_king (bool): Indicates if the piece is a king.
            start (int): Starting row index.
            stop (int): Stopping row index.
            step (int): Step value for row traversal (1 for downward, -1 for upward).
            color (int): Color of the piece.
            left (int): Column index of the leftmost position to search.
            skipped (list): List of pieces to be skipped in the current traversal path.
            
        Returns:
            dict: Dictionary of valid moves.
        """
        moves = {}
        last = []

        for r in range(start, stop, step):
            if right >= COLS:
                break

            current = self.get_piece(r, right)

            if current in skipped:
                break
            elif current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last

                if last:
                    if step == -1:
                        row = max(r-3, -1)
                    else:
                        row = min(r+3, ROWS)

                    moves.update(self._search_left(is_king, r+step, row, step, color, right-1, skipped=moves[(r, right)]))
                    moves.update(self._search_right(is_king, r+step, row, step, color, right+1, skipped=moves[(r, right)]))

                    if is_king:

                        if step == -1:
                            row = min(r+3, ROWS)
                        else:
                            row = max(r-3, -1)

                        moves.update(self._search_left(is_king, r-step, row, -step, color, right-1, skipped=moves[(r, right)]))
                        moves.update(self._search_right(is_king, r-step, row, -step, color, right+1, skipped=moves[(r, right)]))

                break
            elif current.color == color:
                break
            else:
                last = [current]


            right += 1

        return moves
            
    def get_all_moves(self, color):
        """ Returns all possible moves for a color in a single array. """
        moves = []

        for piece in self.get_all_pieces(color):
            valid_moves = self.get_valid_moves(piece)
            moves.extend(valid_moves)

        return moves

class Game:
    """
    Class representing the main game logic for a Tic-Tac-Toe game.

    Attributes:
        win (pygame.display): The Pygame display window.
        board (list): The 2D list representing the game board.
        turn (int): The current turn, either 0 or 1, where 0 represents the player and 1 represents the AI.
        player (int): The player's game piece, either 1 or -1, where 1 represents 'X' and -1 represents 'O'.
        AI (int): The AI's game piece, either 1 or -1, where 1 represents 'X' and -1 represents 'O'.
        FPS (int): The frames per second for the game loop.

    Methods:
        __init__(self): Initializes the Game object and sets up the Pygame display.
        draw_board(self): Draws the game board on the display.
        get_row_col_from_mouse(self, pos): Converts mouse position to game board row and column.
        winner(self): Determines the winner of the game, if any.
        select(self, row, col): Handles player's selection of a game piece.
        update(self): Updates the game state after each turn.
        run(self): Main game loop that handles game events, updates game state, and manages game display.
    """
    
    def __init__(self, win: pygame.surface.Surface, FPS = 60, history_length = 15, ai = True, ai_intelligence=4) -> None:
        """
        Initialize the Game object.

        Args:
            win (pygame.surface.Surface): The pygame window surface to draw the game on.
            FPS (int, optional): The frames per second for the game loop. Defaults to 60.
            history_length (int, optional): The length of the board history for AI move calculations. Defaults to 15.
            ai (bool, optional): Whether to enable AI player or not. Defaults to True.
            ai_intelligence (int, optional): The intelligence level of the AI player. Higher value means smarter AI. 
                Defaults to 4.
        """
        self.win = win
        self.FPS = FPS
        self.history_length = history_length
        self.ai = ai
        self.ai_intelligence = ai_intelligence
        self.games_played = 0
        self.white_wins = self.black_wins = 0
        self._init()
        
    def update(self):
        """
        Update the game state and redraw the game window.
        """
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def _init(self):
        """
        Initialize the game state.
        """
        self.selected = None
        self.board = Board()
        self.turn = WHITE
        self.valid_moves = {}
        self.board_history = []

    def winner(self):
        """
        Check if there is a winner in the game.

        Returns:
            int: The color of the winner, or None if there is no winner yet.
        """
        return self.board.winner()

    def reset(self):
        """
        Reset the game state.
        """
        self._init()

    def select(self, row, col):
        """
        Select a piece on the board.

        Args:
            row (int): The row index of the selected piece.
            col (int): The column index of the selected piece.

        Returns:
            bool: True if a valid piece was selected, False otherwise.
        """
        
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.valid_moves = {}
                self.select(row, col)
        
        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            skip_stat = self.get_skip_status(self.turn)
            self.valid_moves, skp = self.board.get_valid_moves(piece)
            
            if(skip_stat and not skp):
                self.selected = None
                self.valid_moves = {}
                return False
            
            return True
        
        return False


    def _move(self, row, col):
        """
        Move a selected piece to a new position on the board.

        Args:
            row (int): The row index of the destination position.
            col (int): The column index of the destination position.

        Returns:
            bool: True if the move was successful, False otherwise.
        """
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
            self._change_turn()
        else:
            return False
        
        return True
    
    def draw_valid_moves(self, moves):
        """
        Draws circles on the valid moves on the game window.

        Args:
            moves (list): List of valid moves to be drawn on the game window.
        """
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, PASTEL, (col * SQUARE_SIZE + SQUARE_SIZE//2 + BOARD_OFFSET, row * SQUARE_SIZE + SQUARE_SIZE//2 + BOARD_OFFSET),8)
    
    def _change_turn(self):
        """
        Helper method to change the turn from one player to another.
        """
        self.valid_moves = {}
        self.selected=None
        if self.turn == WHITE:
            self.turn = BLACK
            if self.ai:
                self.ai_move()
        else:
            self.turn = WHITE

    def get_board(self):
        """
        Returns the current game board.

        Returns:
            list: Current game board state.
        """
        return self.board
    
    def prepare_board_state(self, board):
        """
        Prepares the game board state for AI move calculation.

        Args:
            board (list): Current game board state.

        Returns:
            list: Prepared game board state for AI move calculation.
        """

        for row in board:
            for piece in row:
                if piece == 0:
                    continue
                elif piece.color == WHITE:
                    board[piece.row][piece.col] = 0
                elif piece.king:
                    board[piece.row][piece.col] = 'BK'
                else:
                    board[piece.row][piece.col] = 'B'

        return board

    
    def ai_move(self):
        """
        Executes the AI's move.

        Uses the minimax algorithm to determine the best move for the AI player.
        """

        value, new_board = minimax(self.get_board(), self.ai_intelligence, True, self)
        if not new_board:
            return
        
        self.board = new_board

        temp_board = deepcopy(new_board.board)

        temp_board = self.prepare_board_state(temp_board)

        self.board_history = [temp_board] + self.board_history

        if len(self.board_history) > self.history_length:
            self.board_history.pop()
            
        self._change_turn()

    def get_position(self,pos):
        """
        Returns the row and column of the game board from the mouse position.

        Args:
            pos (tuple): Tuple containing x and y coordinates of the mouse position.

        Returns:
            int: The row index (0 to 7) on the game board.
            int: The column index (0 to 7) on the game board.
        """
        x, y = pos

        if x < BOARD_OFFSET or y < BOARD_OFFSET or x > BOARD_WIDTH + BOARD_OFFSET or y > BOARD_WIDTH + BOARD_OFFSET:
            return -1, -1

        row = (y - BOARD_OFFSET)// SQUARE_SIZE
        col = (x - BOARD_OFFSET)// SQUARE_SIZE

        return row, col
    
    def get_skip_status(self, color):
        """
        Checks if any piece of the specified color has valid moves that involve skipping over opponent's pieces.

            Args:
            color (str): The color of the pieces to check for valid moves. Should be either "WHITE" or "BLACK".

            Returns:
            bool: True if at least one piece of the specified color has valid moves that involve skipping over opponent's pieces, False otherwise.
        """
        skp = False

        #  Iterate over all pieces of the specified color
        for piece in self.board.get_all_pieces(color):
            valid_moves, skipped = self.board.get_valid_moves(piece)
            #  If any piece has valid moves that involve skipping over opponent's pieces, set skp to True
            if skipped:
                skp = True

        return skp

    def run(self):
        """
        Main game loop that handles game events, updates game state, and manages game display.

        Returns:
            None
        """
        run = True
        clock = pygame.time.Clock()

        while run:
            clock.tick(self.FPS)

            # Check for game winner
            if self.winner() is not None:

                # Display winner message
                pygame.font.init()
                font = pygame.font.SysFont(None, 128)

                if self.winner() == WHITE:
                    self.win.fill(WHITE)
                    win_text = font.render("You win!", True, BLACK)
                else:
                    self.win.fill(BLACK)
                    win_text = font.render("AI wins!", True, WHITE)

                self.win.blit(win_text, ((WIDTH - win_text.get_width()) // 2, (HEIGHT - win_text.get_height()) // 2))

                pygame.display.update()
                sleep(2)

                run = False
                break

            # Handle game events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    row, col = self.get_position(pos)
                    if row != -1 and col != -1:
                        self.select(row, col)

            # Update game state
            self.update()
            pygame.display.update()

        pygame.quit()


def main(WIN, FPS):
    
    #  Creating a game object.
    #  with window and appropriate FPS. 
    game = Game(WIN, FPS)

    #  Running the game
    game.run()

if __name__ == '__main__':

    FPS = 60

    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Checkers')

    main(WIN, FPS)