class Move:
    def __init__(self, start_square, end_square, board):
        self.start_row = start_square[0]
        self.start_col = start_square[1]
        self.end_row = end_square[0]
        self.end_col = end_square[1]
        
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        
    def get_chess_notation(self):

        c_to_files = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}
        r_to_ranks = {0: '8', 1: '7', 2: '6', 3: '5', 4: '4', 5: '3', 6: '2', 7: '1'}
        
        start_file = c_to_files[self.start_col]
        start_rank = r_to_ranks[self.start_row]
        end_file = c_to_files[self.end_col]
        end_rank = r_to_ranks[self.end_row]
        
        return f"{start_file}{start_rank}:{end_file}{end_rank}"