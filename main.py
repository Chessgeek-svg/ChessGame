# %%
import chess

# %%
board = chess.Board()
board.legal_moves

# %%
board = [
    ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
    ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
    ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
]

# %%
class GameState (object):
    def __init__ (self, board, white_to_move, move_log):
        self.board = board
        self.white_to_move = white_to_move
        self.move_log = move_log
    def make_move(self, board, start_row, start_col, end_row, end_col, white_to_move):
        board[end_row][end_col] = board[start_row][start_col]
        board[start_row][start_col] = 0
        white_to_move = not white_to_move

# %%
game = GameState(board, True, [])
game.make_move(board, 0, 0, 4, 4, True)

# %%
print(board)

# %%



