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
        
    def test_check(self):
        #Test with pawn
        self.setup_method()
        self.board[1][3] = 'P'
        self.game.white_to_move = False
        candidate_moves = []
        legal_moves = []
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == 0:
                    continue
                if self.board[i][j].isupper() == self.game.white_to_move:
                    candidate_moves.extend(move_generator.get_moves(self.game, self.board, i, j))
        for move in candidate_moves:
            if not move_generator.puts_in_check(self.game, self.board, move):
                legal_moves.append(move)

        move_list = []
        move_list.extend(move.get_computer_notation() for move in legal_moves)
        assert len(legal_moves) == 4
        assert move_list == ['b8:d7', 'c8:d7', 'd8:d7', 'e8:d7']
        
        #Test with bishop
        self.setup_method()
        self.board[1][3] = 0
        self.board[4][0] = 'B'
        self.game.white_to_move = False
        candidate_moves = []
        legal_moves = []
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == 0:
                    continue
                if self.board[i][j].isupper() == self.game.white_to_move:
                    candidate_moves.extend(move_generator.get_moves(self.game, self.board, i, j))
        for move in candidate_moves:
            if not move_generator.puts_in_check(self.game, self.board, move):
                legal_moves.append(move)

        move_list = []
        move_list.extend(move.get_computer_notation() for move in legal_moves)
        assert len(legal_moves) == 6
        assert move_list == ['b8:d7', 'b8:c6', 'c8:d7', 'd8:d7', 'b7:b5', 'c7:c6']
        
        #Test with knight
        self.setup_method()
        self.board[1][3] = 'P'
        self.game.white_to_move = False
        candidate_moves = []
        legal_moves = []
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == 0:
                    continue
                if self.board[i][j].isupper() == self.game.white_to_move:
                    candidate_moves.extend(move_generator.get_moves(self.game, self.board, i, j))
        for move in candidate_moves:
            if not move_generator.puts_in_check(self.game, self.board, move):
                legal_moves.append(move)

        move_list = []
        move_list.extend(move.get_computer_notation() for move in legal_moves)
        assert len(legal_moves) == 4
        assert move_list == ['b8:d7', 'c8:d7', 'd8:d7', 'e8:d7']
        
        #Test with rook
        self.setup_method()
        self.board[1][4] = 'R'
        self.game.white_to_move = False
        candidate_moves = []
        legal_moves = []
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == 0:
                    continue
                if self.board[i][j].isupper() == self.game.white_to_move:
                    candidate_moves.extend(move_generator.get_moves(self.game, self.board, i, j))
        for move in candidate_moves:
            if not move_generator.puts_in_check(self.game, self.board, move):
                legal_moves.append(move)

        move_list = []
        move_list.extend(move.get_computer_notation() for move in legal_moves)
        assert len(legal_moves) == 4
        assert move_list == ['d8:e7', 'e8:e7', 'f8:e7', 'g8:e7']
        
        #en passant should be illegal if it puts the player in check
        self.setup_method()
        self.board[1][0] = 0
        self.board[3][0] = 'P'
        self.board[3][1] = 'p'
        self.board[4][0] = 'K'
        self.board[7][4] = 0
        self.board[6][4] = 0
        self.game.en_passant = [2,1]
        candidate_moves = []
        legal_moves = []
                
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == 0:
                    continue
                if self.board[i][j].isupper() == self.game.white_to_move:
                    candidate_moves.extend(move_generator.get_moves(self.game, self.board, i, j))
        for move in candidate_moves:
            if not move_generator.puts_in_check(self.game, self.board, move):
                legal_moves.append(move)
        
        move_list = []
        move_list.extend(move.get_computer_notation() for move in legal_moves)
        assert len(legal_moves) == 5
        assert move_list == ['a4:a3', 'a4:b4', 'a4:b5', 'a4:b3', 'f1:b5']
        #en passant is not possible because it would result in check
        
        #if the check from the rook were blocked, en passant would be possible:
        candidate_moves = []
        legal_moves = []
        self.board[1][0] = 'p'
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == 0:
                    continue
                if self.board[i][j].isupper() == self.game.white_to_move:
                    candidate_moves.extend(move_generator.get_moves(self.game, self.board, i, j))
        for move in candidate_moves:
            if not move_generator.puts_in_check(self.game, self.board, move):
                legal_moves.append(move)
        
        move_list = []
        move_list.extend(move.get_computer_notation() for move in legal_moves)
        assert len(legal_moves) == 6
        assert move_list == ['a5:b6', 'a4:a3', 'a4:b4', 'a4:b5', 'a4:b3', 'f1:b5']

    def test_promotion(self):
        #Promotion is possible when reaching the final rank, by capture or otherwise
        self.setup_method()
        self.board[1][2] = 'P'
        self.board[0][2] = 0
        moves_for_piece = move_generator.get_pawn_moves(self.game, self.board, 1, 2)
        assert len(moves_for_piece) == 12
        move_list = []
        move_list.extend(move.get_computer_notation() for move in moves_for_piece)
        assert move_list == ['c7:c8=Q', 'c7:c8=R', 'c7:c8=B', 'c7:c8=N', 
                             'c7:b8=Q', 'c7:b8=R', 'c7:b8=B', 'c7:b8=N', 
                             'c7:d8=Q', 'c7:d8=R', 'c7:d8=B', 'c7:d8=N']

        #Promotion is not possible for non-pawn pieces
        self.setup_method()
        self.board[1][0] = 'B'
        self.board[2][1] = 'P'
        moves_for_piece = move_generator.get_bishop_moves(self.game, self.board, 1, 0)
        move_list = []
        move_list.extend(move.get_computer_notation() for move in moves_for_piece)
        assert move_list == ['a7:b8']
        assert len(moves_for_piece) == 1

        #Promotion can only occur at the end of the board
        moves_for_piece = move_generator.get_moves(self.game, self.board, 2, 1)
        move_list = []
        move_list.extend(move.get_computer_notation() for move in moves_for_piece)
        assert move_list == ['b6:c7']
        assert len(moves_for_piece) == 1

        #Both colors can promote
        self.setup_method()
        self.board[6][0] = 'p'
        moves_for_piece = move_generator.get_pawn_moves(self.game, self.board, 6, 0)
        move_list = []
        move_list.extend(move.get_computer_notation() for move in moves_for_piece)
        assert move_list == ['a2:b1=q', 'a2:b1=r', 'a2:b1=b', 'a2:b1=n']
        assert len(moves_for_piece) == 4
