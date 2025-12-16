import move_generator
from Move import Move

starting_board = [
            ['r', 'n', 'b', 'q', 'k',  0 ,  0 , 'r'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            [ 0 ,  0 ,  0 ,  0 ,  0 ,  0 ,  0 ,  0],
            [ 0 ,  0 ,  0 ,  0 ,  0 ,  0 ,  0 ,  0],
            [ 0 ,  0 ,  0 ,  0 ,  0 ,  0 ,  0 ,  0],
            [ 0 ,  0 ,  0 ,  0 ,  0 ,  0 ,  0 ,  0],
            [ 0 ,  0 ,  0 ,  0 ,  0 ,  0 ,  0 ,  0],
            ['R',  0 ,  0 ,  0 , 'K',  0 ,  0 , 'R']
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
        if not self.candidate_moves:
            print(self.checkmate_stalemate())
        temp = Move((start_row, start_col), (end_row, end_col), self.board, promote_to)
        if temp in self.candidate_moves:
            is_castle = self.castle_move(start_row, start_col, end_col)
            #Promotion check naively assumes that if a piece is passed in, it is possible to promote
            self.board[end_row][end_col] = promote_to if promote_to else self.board[start_row][start_col]
            self.board[start_row][start_col] = 0
            #Check if move is en passant, remove captured piece if so
            if self.board[end_row][end_col].upper() == 'P' and [end_row, end_col] == self.en_passant:
                self.board[start_row][end_col] = 0
            #If move is castle, update board to move the rook
            if is_castle:
                if start_col - end_col == 2:
                    self.board[end_row][3] = self.board[end_row][0]
                    self.board[end_row][0] = 0
                elif start_col - end_col == -2:
                    self.board[end_row][5] = self.board[end_row][7]
                    self.board[end_row][7] = 0
                else:
                    print("Error, illegal / impossible castle")
            self.en_passant = move_generator.check_en_passant(self.board, start_row, end_row, end_col)
            self.candidate_moves = []
            self.move_log.append(Move.get_computer_notation(temp))
            self.white_to_move = not self.white_to_move
            print(self.board)
        else:
            print("Illegal Move")
        for i in range(0,8):
            for j in range(0,8):
                if self.board[i][j] == 0:
                    continue
                if self.board[i][j].isupper() == self.white_to_move:
                    moves_for_piece = move_generator.get_moves(self, self.board, i, j)
                    self.candidate_moves.extend(moves_for_piece)
    def castle_move(self, start_row, start_col, end_col):
        if self.board[start_row][start_col].upper() == "K" and abs(start_col - end_col) == 2:
            return True
        return False
    def checkmate_stalemate(self):
        for i in range(0,8):
            for j in range(0,8):
                if self.board[i][j] == 0:
                    continue
                if self.board[i][j].isupper() == self.white_to_move:
                    moves_for_piece = move_generator.get_moves(self, self.board, i, j)
                    if moves_for_piece:
                        pass_move = Move((0, 0), (0, 0), self.board)
                        if move_generator.puts_in_check(self, self.board, pass_move):                        
                            return "Check"
                        return "Normal"
        
        pass_move = Move((0, 0), (0, 0), self.board)
        if move_generator.puts_in_check(self, self.board, pass_move):
            return "Checkmate"
        return "Stalemate"

game = GameState(white_to_move = True, move_log = ['e1:d1'])

for i in range(0,8):
    for j in range(0,8):
        if game.board[i][j] == 0:
            continue
        if game.board[i][j].isupper() == game.white_to_move:
            moves_for_piece = move_generator.get_moves(game, game.board, i, j)
            game.candidate_moves.extend(moves_for_piece)
            
print([move.get_computer_notation() for move in game.candidate_moves])
#Example of illegal & legal move behavior respectively
game.make_move(7, 4, 7, 2, "Q")
game.make_move(7, 4, 7, 6)
