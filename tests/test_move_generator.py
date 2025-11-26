import move_generator
from main import GameState
    
class TestMoveGeneration:
    def setup_method(self):
        self.board = [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        ]
        self.game = GameState(self.board, white_to_move = True, move_log = [])


    def test_rook_moves(self):
        self.setup_method()
        self.board[6][7] = 0
        
        #Test a trapped rook
        assert move_generator.get_rook_moves(self.game, self.board, 7, 0) == []
        
        #Test a rook that can move and capture
        moves_for_piece = move_generator.get_rook_moves(self.game, self.board, 7, 7)
        assert len(moves_for_piece) == 6
        move_list =  []
        move_list.extend(move.get_computer_notation() for move in moves_for_piece)
        assert move_list == ['h1:h2',  'h1:h3', 'h1:h4', 'h1:h5', 'h1:h6', 'h1:h7']
        
    def test_bishop_moves(self):
        self.setup_method()
        self.board[6][6] = 0
        self.board[6][4] = 'p'
        
        #Test a trapped bishop
        assert move_generator.get_bishop_moves(self.game, self.board, 7, 2) == []
        
        #Test a bishop that can move and capture
        moves_for_piece = move_generator.get_bishop_moves(self.game, self.board, 7, 5)
        assert len(moves_for_piece) == 3
        move_list =  []
        move_list.extend(move.get_computer_notation() for move in moves_for_piece)
        assert move_list == ['f1:e2', 'f1:g2', 'f1:h3']
        
    def test_queen_moves(self):
        self.setup_method()
        self.board[4][3] = 'Q'
        
        #Test a trapped Queen
        assert move_generator.get_queen_moves(self.game, self.board, 7, 3) == []
        
        #Test a Queen that can move and capture        
        moves_for_piece = move_generator.get_queen_moves(self.game, self.board, 4, 3)
        assert len( moves_for_piece) == 19
        move_list = []
        move_list.extend(move.get_computer_notation() for move in moves_for_piece)
        assert move_list == ['d4:d5', 'd4:d6', 'd4:d7', 'd4:d3', 'd4:c4', 'd4:b4', 'd4:a4', 'd4:e4', 'd4:f4', 'd4:g4', 'd4:h4', 'd4:c5', 'd4:b6', 'd4:a7', 'd4:e5', 'd4:f6', 'd4:g7', 'd4:c3', 'd4:e3']
        
    def test_knight_moves(self):
        self.setup_method()
        self.board[5][0] = 'P'
        self.board[5][2] = 'N'
        
        #Test a trapped knight
        assert move_generator.get_knight_moves(self.game, self.board, 7, 1) == []
        
        #Test a knight that can move and capture
        moves_for_piece = move_generator.get_knight_moves(self.game, self.board, 5, 2)
        assert len(moves_for_piece) == 4
        move_list = []
        move_list.extend(move.get_computer_notation() for move in moves_for_piece)
        assert move_list == ['c3:b5', 'c3:d5', 'c3:a4', 'c3:e4']
        
    def test_king_moves(self):
        self.setup_method()
        self.board[4][4] = 'K'
        
        #Test a trapped king
        assert move_generator.get_king_moves(self.game, self.board, 7, 4) == []
        
        #Test a king that can move and capture
        moves_for_piece = move_generator.get_king_moves(self.game, self.board, 4, 4)
        assert len(moves_for_piece) == 8
        move_list = []
        move_list.extend(move.get_computer_notation() for move in moves_for_piece)
        assert move_list == ['e4:e5', 'e4:e3', 'e4:d4', 'e4:f4', 'e4:d5', 'e4:f5', 'e4:d3', 'e4:f3']
        
    def test_pawn_moves(self):
        self.setup_method()
        self.board[5][0] = 'p'
        
        #Test a blocked pawn
        assert move_generator.get_pawn_moves(self.game, self.board, 6, 0) == []
        
        #Test a pawn that can move and capture
        moves_for_piece = move_generator.get_pawn_moves(self.game, self.board, 6, 1)
        assert len(moves_for_piece) == 3
        move_list = []
        move_list.extend(move.get_computer_notation() for move in moves_for_piece)
        assert move_list == ['b2:b3', 'b2:b4', 'b2:a3']
        
    def test_en_passant(self):
        self.setup_method()
        self.board[3][0] = 'P'
        self.board[3][1] = 'p'
        self.game.en_passant = [2, 1]
        
        moves_for_piece = move_generator.get_pawn_moves(self.game, self.board, 3, 0)
        assert len(moves_for_piece) == 2
        move_list = []
        move_list.extend(move.get_computer_notation() for move in moves_for_piece)
        assert move_list == ['a5:a6', 'a5:b6']
        
        self.game.candidate_moves = moves_for_piece
        self.game.make_move(3, 0, 2, 1)
        assert self.board[2][1] == 'P'
        assert self.board[3][1] == 0
        assert self.game.en_passant == False