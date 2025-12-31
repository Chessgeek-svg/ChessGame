class Move:
    C_TO_FILES = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}
    R_TO_RANKS = {0: '8', 1: '7', 2: '6', 3: '5', 4: '4', 5: '3', 6: '2', 7: '1'}
    piece_notation = {'P': '',  'R': 'R', 'N': 'N', 'B': 'B', 'Q': 'Q', 'K': 'K'}
    
    def __init__(self, start_square, end_square, board, is_en_passant=False, is_castle=False, promote_to=None):
        self.start_row, self.start_col = start_square
        self.end_row, self.end_col = end_square
        self.is_en_passant = is_en_passant
        self.is_castle = is_castle
        self.promote_to = promote_to
        self.promoted_piece_ref = None
        
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]

        if self.is_en_passant:
            self.piece_captured = board[self.start_row][self.end_col]
        
        self.move_id = self.start_row * 10000 + self.start_col * 1000 + self.end_row * 100 + self.end_col * 10
        
    def get_computer_notation(self):   
        start_file = Move.C_TO_FILES[self.start_col]
        start_rank = Move.R_TO_RANKS[self.start_row]
        end_file = Move.C_TO_FILES[self.end_col]
        end_rank = Move.R_TO_RANKS[self.end_row]

        if self.promote_to:
            return f"{start_file}{start_rank}:{end_file}{end_rank}={self.promote_to}"
        
        return f"{start_file}{start_rank}:{end_file}{end_rank}"
    
    def get_algebraic_notation(self):
        if self.is_castle:
            return "0-0-0" if self.end_col == 2 else "0-0"
        
        piece = Move.piece_notation[str(self.piece_moved)[1].upper()]

        end_file = Move.C_TO_FILES[self.end_col]
        end_rank = Move.R_TO_RANKS[self.end_row]
        capture = "x" if self.piece_captured else ""

        if capture and piece == '':
            piece = Move.C_TO_FILES[self.start_col]

        if self.promote_to:
            return f"{piece}{capture}{end_file}{end_rank}={self.promote_to}"
        
        return f"{piece}{capture}{end_file}{end_rank}"
    
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.move_id == other.move_id
        return False