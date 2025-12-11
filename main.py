import move_generator
from Move import Move

starting_board = [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            [ 0 ,  0 ,  0 ,  0 ,  0 ,  0 ,  0 ,  0],
            [ 0 ,  0 ,  0 ,  0 ,  0 ,  0 ,  0 ,  0],
            [ 0 ,  0 ,  0 ,  0 ,  0 ,  0 ,  0 ,  0],
            [ 0 ,  0 ,  0 ,  0 ,  0 ,  0 ,  0 ,  0],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        ]

class GameState (object):
    def __init__ (self, board = starting_board, white_to_move = True, move_log = []):
        self.board = board            
        self.white_to_move = white_to_move
        self.move_log = move_log
        self.en_passant = []
        self.candidate_moves = []
        self.check_analysis = False
    def make_move(self, start_row, start_col, end_row, end_col, promote_to = None):
        temp = Move((start_row, start_col), (end_row, end_col), self.board, promote_to)
        if temp in self.candidate_moves:
            self.board[end_row][end_col] = promote_to if promote_to else self.board[start_row][start_col]
            self.board[start_row][start_col] = 0
            #Check if move is en passant, remove captured piece if so
            if self.board[end_row][end_col].upper() == 'P' and [end_row, end_col] == self.en_passant:
                self.board[start_row][end_col] = 0
            self.en_passant = move_generator.check_en_passant(self.board, start_row, end_row, end_col)
            self.candidate_moves = []
            game.white_to_move = not game.white_to_move
            print(game.board)
        else:
            print("Illegal Move")

game = GameState(white_to_move = True, move_log = [])

for i in range(0,8):
    for j in range(0,8):
        if game.board[i][j] == 0:
            continue
        if game.board[i][j].isupper() == game.white_to_move:
            moves_for_piece = move_generator.get_moves(game, game.board, i, j)
            game.candidate_moves.extend(moves_for_piece)
            
print([move.get_computer_notation() for move in game.candidate_moves])
#Example of illegal & legal move behavior respectively
game.make_move(1, 1, 0, 2, "Q")
game.make_move(6, 4, 4, 4)
