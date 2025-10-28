import move_generator
from Move import Move

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

class GameState (object):
    def __init__ (self, board, white_to_move, move_log):
        self.board = board
        self.white_to_move = white_to_move
        self.move_log = move_log
        self.en_passant = [2,1]
    def make_move(self, start_row, start_col, end_row, end_col):
        temp = Move((start_row, start_col), (end_row, end_col), board)
        if temp in candidate_moves:
            board[end_row][end_col] = board[start_row][start_col]
            board[start_row][start_col] = 0
            #Check if move is en passant, remove captured piece if so
            if board[end_row][end_col].upper() == 'P' and [end_row, end_col] == self.en_passant:
                board[start_row][end_col] = 0
            self.en_passant = move_generator.check_en_passant(board, start_row, end_row, end_col)
            game.white_to_move = not game.white_to_move
            print(game.board)
        else:
            print("Illegal Move")

game = GameState(board, True, [])

candidate_moves = []
for i in range(0,8):
    for j in range(0,8):
        if board[i][j] == 0:
            continue
        if board[i][j].isupper() == game.white_to_move:
            moves_for_piece = move_generator.get_moves(game, board, i, j)
            candidate_moves.extend(moves_for_piece)
            
print([move.get_computer_notation() for move in candidate_moves])
#Example of illegal & legal move behavior respectively
game.make_move(3, 0, 2, 1)
game.make_move(6, 4, 4, 4)
