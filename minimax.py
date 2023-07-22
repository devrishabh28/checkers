from copy import deepcopy
import math
from constants import WHITE, BLACK

def minimax(position, depth, max_player, game, alpha=-math.inf, beta=math.inf):
    """
    Minimax algorithm with alpha-beta pruning for game playing AI.

    Args:
        position: Current game state or position.
        depth: Depth of the current search in the game tree.
        max_player: True if the current player is maximizing player, False if minimizing player.
        game: The game object containing game rules and state.
        alpha: The alpha value for alpha-beta pruning. Default is negative infinity.
        beta: The beta value for alpha-beta pruning. Default is positive infinity.

    Returns:
        best_score: The best score found by the algorithm.
        best_move: The best move found by the algorithm.
    """

    if depth == 0 or position.winner() is not None:
        pos = deepcopy(position.board)

        if game.prepare_board_state(pos) in game.board_history:
            return position.evaluate()/(len(game.board_history) - (game.board_history.index(pos))), position

        return position.evaluate(), position
    
    if max_player:
        best_score = -math.inf
        best_move = None
        for move in get_all_moves(position, BLACK, game):
            score = minimax(move, depth-1, not max_player, game, alpha, beta)[0]

            if score >= best_score:
                best_score = score
                best_move = move

            alpha = max(alpha, best_score)
            if beta <= alpha:
                break

        return best_score, best_move
    else:
        best_score = math.inf
        best_move = None
        for move in get_all_moves(position, WHITE, game):
            score = minimax(move, depth-1, not max_player, game, alpha, beta)[0]

            if score <= best_score:
                best_score = score
                best_move = move

            beta = min(beta, best_score)
            if beta <= alpha:
                break

        return best_score, best_move

def simulate_move(piece, move, board, game, skip):
    """
    Simulates a move on the board.

    Args:
        piece: The piece to be moved.
        move: The move to be made.
        board: The current game board state.
        game: The game object containing game rules and state.
        skip: The piece to be skipped during the move (if any).

    Returns:
        board: The updated game board state after making the move.
    """
    board.move(piece, *move)
    if skip:
        board.remove(skip)

    return board

def get_all_moves(board, color, game):
    """
    Get all possible moves for a given color on the board.

    Args:
        board: The current game board state.
        color: The color of the pieces to be moved.
        game: The game object containing game rules and state.

    Returns:
        moves: A list of all possible game board states after making each move.
    """
    moves = []
    skp = False

    for piece in board.get_all_pieces(color):
        valid_moves, skipped = board.get_valid_moves(piece)
        if skipped:
            skp = True

    for piece in board.get_all_pieces(color):
        valid_moves, skipped = board.get_valid_moves(piece)
        if skp and not skipped:
            continue
        for move, skip in valid_moves.items():
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_move(temp_piece, move, temp_board, game, skip)
            moves.append(new_board)

    return moves
