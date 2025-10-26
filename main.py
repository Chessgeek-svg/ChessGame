import move_generator
board = [
    ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
    ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
    [0, 0, 0, 0, 0, 0, 0, 0],
    ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
]

class GameState (object):
    def __init__ (self, board, white_to_move, move_log):
        self.board = board
        self.white_to_move = white_to_move
        self.move_log = move_log
    def make_move(self, start_row, start_col, end_row, end_col, white_to_move):
        board[end_row][end_col] = board[start_row][start_col]
        board[start_row][start_col] = 0
        white_to_move = not white_to_move

game = GameState(board, True, [])

candidate_moves = []
for i in range(0,8):
    for j in range(0,8):
        if board[i][j] == 0:
            continue
        if board[i][j].isupper() == game.white_to_move:
            moves_for_piece = move_generator.get_moves(game, board, i, j)
            candidate_moves.extend(moves_for_piece)
            
print([move.get_chess_notation() for move in candidate_moves])
#game.make_move(0, 0, 4, 4, True)

#print(board)


