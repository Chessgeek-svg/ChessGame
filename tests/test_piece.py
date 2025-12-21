from Gamestate import Gamestate
from Move import Move
from Piece import Rook, Pawn, Queen, King, Knight, Bishop

class TestPiece:
    def setup_method(self):
        self.game = Gamestate(setup_type="empty")

    def test_rook_moves(self):
        self.setup_method()
        rook = Rook("White", (2, 3))
        self.game.place_piece_manually(rook, (2, 3))

        assert isinstance(rook, Rook), "rook added is not an instance of the Rook class"
        assert rook.color == "White", "Rook color not stored correctly"

        moves = rook.get_legal_moves(self.game)
        notation_list = [move.get_computer_notation() for move in moves]
        expected = ['d6:d5', 'd6:d4', 'd6:d3', 'd6:d2', 'd6:d1', 'd6:d7', 'd6:d8',
                    'd6:e6', 'd6:f6', 'd6:g6', 'd6:h6', 'd6:c6', 'd6:b6', 'd6:a6']

        assert len(notation_list) == 14, "Incorrect number of rook moves generated"
        assert set(notation_list) == set(expected), "Wrong rook moves generated"

    def test_bishop_moves(self):
        self.setup_method()        
        bishop = Bishop("Black", (4, 4))
        self.game.place_piece_manually(bishop, (4, 4))

        moves = bishop.get_legal_moves(self.game)
        notation_list = [move.get_computer_notation() for move in moves]
        expected = ['e4:f3', 'e4:g2', 'e4:h1', 'e4:d5', 'e4:c6', 'e4:b7', 'e4:a8',
                    'e4:d3', 'e4:c2', 'e4:b1', 'e4:f5', 'e4:g6', 'e4:h7']
        
        assert len(notation_list) == 13, "Incorrect number of bishop moves generated"
        assert set(notation_list) == set(expected), "Wrong bishop moves generated"

    def test_queen_moves(self):
        self.setup_method()        
        queen = Queen("White", (1, 1))
        self.game.place_piece_manually(queen, (1, 1))

        moves = queen.get_legal_moves(self.game)
        notation_list = [move.get_computer_notation() for move in moves]
        expected = ['b7:a8', 'b7:c6', 'b7:d5', 'b7:e4', 'b7:f3', 'b7:g2', 'b7:h1', 'b7:a6',
                    'b7:c8', 'b7:b1', 'b7:b2', 'b7:b3', 'b7:b4', 'b7:b5', 'b7:b6', 'b7:b8',
                    'b7:a7', 'b7:c7', 'b7:d7', 'b7:e7', 'b7:f7', 'b7:g7', 'b7:h7']
        
        assert len(notation_list) == 23, "Incorrect number of queen moves generated"
        assert set(notation_list) == set(expected), "Wrong queen moves generated"

    def test_knight_moves(self):
        self.setup_method()        
        knight = Knight("Black", (4, 4))
        self.game.place_piece_manually(knight, (4, 4))

        moves = knight.get_legal_moves(self.game)
        notation_list = [move.get_computer_notation() for move in moves]
        expected = ['e4:d6', 'e4:c5', 'e4:c3', 'e4:d2', 'e4:f2', 'e4:g3', 'e4:g5', 'e4:f6']
        
        assert len(notation_list) == 8, "Incorrect number of knight moves generated"
        assert set(notation_list) == set(expected), "Wrong knight moves generated"

    def test_pawn_moves(self):
        self.setup_method()
        self.game.place_piece_manually(Pawn("White", (6, 6)), (6, 6)) #White pawn on g2
        self.game.place_piece_manually(Pawn("Black", (5, 7)), (5, 7)) #Black pawn on h3
        self.game.place_piece_manually(Pawn("Black", (4, 5)), (4, 5)) #Black pawn on f4
        self.game.place_piece_manually(Pawn("Black", (6, 7)), (6, 7)) #Black pawn on h2
        self.game.place_piece_manually(Rook("White", (7, 6)), (7, 6)) #White rook on g1


        #Test normal and starting square pawn moves / captures
        moves = self.game.board[6][6].get_legal_moves(self.game)
        notation_list = [move.get_computer_notation() for move in moves]
        expected = ['g2:g4', 'g2:g3', 'g2:h3']

        assert len(notation_list) == 3, "Incorrect number of pawn moves generated"
        assert set(notation_list) == set(expected), "Wrong pawn moves generated"


        #Test en passant
        self.game.make_move(Move((6, 6), (4, 6), self.game.board))
        moves = self.game.board[4][5].get_legal_moves(self.game)
        notation_list = [move.get_computer_notation() for move in moves]
        expected = ['f4:f3', 'f4:g3']

        assert len(notation_list) == 2, "Incorrect number of pawn moves generated (en passant scenario)"
        assert set(notation_list) == set(expected), "Wrong pawn moves generated (en passant scenario)"

        #Test promotion
        moves = self.game.board[6][7].get_legal_moves(self.game)
        notation_list = [move.get_computer_notation() for move in moves]
        expected = ['h2:h1=Q', 'h2:h1=R', 'h2:h1=B', 'h2:h1=N', 'h2:g1=Q', 'h2:g1=R', 'h2:g1=B', 'h2:g1=N']

        assert len(notation_list) == 8, "Incorrect number of pawn moves generated (promotion scenario)"
        assert set(notation_list) == set(expected), "Wrong pawn moves generated (promotion scenario)"

    def test_king_moves(self):
        self.setup_method()
        self.game.place_piece_manually(King("White", (7, 4)), (7, 4)) #White pawn on g2
        self.game.place_piece_manually(Rook("White", (7, 7)), (7, 7)) #White rook on h1
        self.game.place_piece_manually(Rook("White", (7, 0)), (7, 0)) #White rook on a1
        self.game.place_piece_manually(Knight("White", (7, 1)), (7, 1)) #White knight on b1

        #Castling queenside is blocked, castling kingside is legal
        moves = self.game.board[7][4].get_legal_moves(self.game)
        notation_list = [move.get_computer_notation() for move in moves]
        expected = ['e1:d1', 'e1:d2', 'e1:e2','e1:f2', 'e1:f1', 'e1:g1']

        assert len(notation_list) == 6, "Incorrect number of King moves generated"
        assert set(notation_list) == set(expected), "Wrong King moves generated"

        #Unblock queenside castle
        self.game.remove_piece_manually((7,1))
        moves = self.game.board[7][4].get_legal_moves(self.game)
        notation_list = [move.get_computer_notation() for move in moves]
        expected = ['e1:d1', 'e1:d2', 'e1:e2','e1:f2', 'e1:f1', 'e1:g1', 'e1:c1']

        assert len(notation_list) == 7, "Incorrect number of King moves generated"
        assert set(notation_list) == set(expected), "Wrong King moves generated"