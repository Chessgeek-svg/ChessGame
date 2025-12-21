from Move import Move
from Piece import Piece, Pawn, Rook, Knight, Bishop, Queen, King

class Gamestate (object):
    def __init__(self, setup_type="standard"):
        self.white_pieces = []
        self.black_pieces = []

        if setup_type == "standard":
            self.board = self._create_starting_board()
            self.white_to_move = True
        else:
            self.board = [
                [None for _ in range(8)] for _ in range(8)
            ]
            self.white_to_move = True
        self.white_king = self.get_piece_by_type(King, "White")
        self.black_king = self.get_piece_by_type(King, "Black")
        self.move_log = []
        self.en_passant_target = None
        self.en_passant_target_log = [] 
        self.castling_rights = {
            'White': {'kingside': True, 'queenside': True},
            'Black': {'kingside': True, 'queenside': True}
        }
        self.castling_rights_log = []

        self.checkmate = False
        self.stalemate = False

    def _create_starting_board(self):
        board = [[None for _ in range(8)] for _ in range(8)]
        
        piece_order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        
        for col in range(8):
            PieceClass = piece_order[col]
            
            # Place Black Pieces (Row 0)
            board[0][col] = PieceClass("Black", (0, col))
            
            # Place White Pieces (Row 7)
            board[7][col] = PieceClass("White", (7, col))
            
            # Place Pawns (Row 1 and 6)
            board[1][col] = Pawn("Black", (1, col))
            board[6][col] = Pawn("White", (6, col))

            self.black_pieces.append(board[0][col])
            self.black_pieces.append(board[1][col])
            self.white_pieces.append(board[7][col])
            self.white_pieces.append(board[6][col])

        return board
    
    def place_piece_manually(self, piece, square):
        row, col = square
        self.board[row][col] = piece
        piece.square = (row, col)

        if piece.color == "White":
            self.white_pieces.append(piece)
            if isinstance(piece, King):
                self.white_king = piece
        else:
            self.black_pieces.append(piece)
            if isinstance(piece, King):
                self.black_king = piece            

    def remove_piece_manually(self, square):
        row, col = square
        piece = self.board[row][col]

        if piece is None:
            return
        
        piece.square = None
        self.board[row][col] = None

        if piece.color == "White":
            self.white_pieces.remove(piece)
        else:
            self.black_pieces.remove(piece)

    def get_piece_by_type(self, piece_type, color):
        target_list = self.white_pieces if color == "White" else self.black_pieces
        for piece in target_list:
            if isinstance(piece, piece_type):
                return piece
        return None

    def make_move(self, move):
        #append previous states to logs
        self.en_passant_target_log.append(self.en_passant_target)
        self.castling_rights_log.append(self._get_castle_rights_copy())

        self.board[move.start_row][move.start_col] = None
        self.board[move.end_row][move.end_col] = move.piece_moved

        if move.piece_captured:
            move.piece_captured.square = None

        move.piece_moved.square = (move.end_row, move.end_col)

        #Create new piece for promotion, set Pawn.square to none
        if move.promote_to:
            move.piece_moved.square = None
            piece_map = {"Q": Queen, "R": Rook, "B": Bishop, "N": Knight}
            NewClass = piece_map[move.promote_to]
            new_piece = NewClass(move.piece_moved.color, (move.end_row, move.end_col))
            self.board[move.end_row][move.end_col] = new_piece
            active_list = self.white_pieces if move.piece_moved.color == "White" else self.black_pieces
            active_list.append(self.board[move.end_row][move.end_col])
            #Store a reference to the new piece, so it can be deleted when undoing this move
            move.promoted_piece_ref = new_piece

        if move.is_en_passant:
            self.board[move.start_row][move.end_col] = None

        if move.is_castle:
            if move.end_col - move.start_col == 2: #Kingside
                rook = self.board[move.end_row][7]
                self.board[move.end_row][7] = None
                self.board[move.end_row][5] = rook
                rook.square = (move.end_row, 5)
            else: # Queenside
                rook = self.board[move.end_row][0]
                self.board[move.end_row][0] = None
                self.board[move.end_row][3] = rook
                rook.square = (move.end_row, 3)

        #Update en passant and castling rights
        if isinstance(move.piece_moved, Pawn) and abs(move.start_row - move.end_row) == 2:
            self.en_passant_target = ((move.start_row + move.end_row) // 2, move.start_col)
        else:
            self.en_passant_target = None
        self.update_castle_rights(move)

        self.move_log.append(move)
        self.white_to_move = not self.white_to_move

    def undo_move(self):
        if len(self.move_log) == 0:
            return
            
        move = self.move_log.pop()

        self.board[move.start_row][move.start_col] = move.piece_moved
        self.board[move.end_row][move.end_col] = None

        move.piece_moved.square = (move.start_row, move.start_col)

        if move.piece_captured:

            if not move.is_en_passant:
                self.board[move.end_row][move.end_col] = move.piece_captured
                move.piece_captured.square = (move.end_row, move.end_col)

            else:
                self.board[move.start_row][move.end_col] = move.piece_captured
                move.piece_captured.square = (move.start_row, move.end_col)


        if move.is_castle:
            if move.end_col - move.start_col == 2: # Kingside
                rook = self.board[move.end_row][5]
                self.board[move.end_row][7] = rook
                self.board[move.end_row][5] = None
                rook.square = (move.end_row, 7)
            else: # Queenside
                rook = self.board[move.end_row][3]
                self.board[move.end_row][0] = rook
                self.board[move.end_row][3] = None
                rook.square = (move.end_row, 0)

        if move.promote_to:
            promoted_piece = move.promoted_piece_ref
            active_list = self.white_pieces if move.piece_moved.color == "White" else self.black_pieces
            active_list.remove(promoted_piece)

        self.white_to_move = not self.white_to_move

        #Reset en passant and castle rights & logs
        self.castling_rights = self.castling_rights_log.pop()
        self.en_passant_target = self.en_passant_target_log.pop()

    #Get moves that would be possible for each piece
    def get_all_valid_moves(self):
        moves = []
        piece_list = self.white_pieces if self.white_to_move else self.black_pieces
        for piece in piece_list:
                if piece.square: #Only check pieces that are on the board
                    moves.extend(piece.get_legal_moves(self))
        return moves
    
    #Valid potential moves to ensure they don't place / leave king in check
    def get_all_legal_moves(self):
        candidate_moves = self.get_all_valid_moves()
        legal_moves = []
        for move in candidate_moves:
            #Do not allow castling through or out of check. 
            #Computationally could be improved (generating every opp move 3 times for each castle option)
            if move.is_castle:
                if (self.square_under_attack((move.start_row, move.start_col)) or 
                self.square_under_attack((move.start_row, (move.start_col + move.end_col) // 2))):
                    continue

            self.make_move(move)
            self.white_to_move = not self.white_to_move
            if not self.in_check():
                legal_moves.append(move)
            self.white_to_move = not self.white_to_move

            self.undo_move()

        return legal_moves

    def in_check(self):          
        king = self.white_king if self.white_to_move else self.black_king
        
        # Safety valve (for empty / illegal board analysis)
        if king is None: 
            return False
        
        return self.square_under_attack(king.square)

    #Currently only useful
    def square_under_attack(self, square):
        r, c = square
        self.white_to_move = not self.white_to_move 
        opponent_moves = self.get_all_valid_moves()
        self.white_to_move = not self.white_to_move
        
        for move in opponent_moves:
            if move.end_row == r and move.end_col == c:
                return True
        return False
    
    def update_castle_rights(self, move):
        if isinstance(move.piece_moved, King):
            self.castling_rights[move.piece_moved.color]['kingside'] = False
            self.castling_rights[move.piece_moved.color]['queenside'] = False
        elif isinstance(move.piece_moved, Rook):
            self._remove_rook_rights(move.piece_moved.color, (move.start_row, move.start_col))
        if isinstance(move.piece_captured, Rook):
            self._remove_rook_rights(move.piece_captured.color, (move.end_row, move.end_col))

    def _remove_rook_rights(self, color, square):
        r, c = square
        start_row = 7 if color == "White" else 0
        if r == start_row:
            if c == 0:
                self.castling_rights[color]['queenside'] = False
            elif c == 7:
                self.castling_rights[color]['kingside'] = False

    def _get_castle_rights_copy(self):
        return {
            'White': self.castling_rights['White'].copy(),
            'Black': self.castling_rights['Black'].copy()
        }