from Gamestate import Gamestate
from Move import Move
from Piece import Rook, Pawn, Queen, King, Knight, Bishop

class TestGameState:
    def setup_method(self):
        self.game = Gamestate(setup_type="standard")

    def test_piece_list_sync(self):
        empty_game = Gamestate(setup_type="empty")
        
        rook = Rook("White", (3, 3))
        empty_game.place_piece_manually(rook, (3, 3))
        
        assert empty_game.board[3][3] == rook
        assert rook in empty_game.white_pieces, "Piece not added to internal list"
        assert len(empty_game.white_pieces) == 1

    def test_castling_rights_logic(self):
        self.setup_method()
        game = self.game
        assert game.castling_rights['White']['kingside'] is True

        move = Move((7, 7), (6, 7), game.board)
        game.make_move(move)

        assert game.castling_rights['White']['kingside'] is False, "Castling rights not lost after rook move"
        
        game.undo_move()
        assert game.castling_rights['White']['kingside'] is True, "Castling rights not restored after undo"

        move = Move((0, 4), (1, 4), game.board)
        game.make_move(move)
        assert game.castling_rights[move.piece_moved.color]['kingside'] is False, "Castling rights not lost after king move"
        assert game.castling_rights[move.piece_moved.color]['queenside'] is False, "Castling rights not lost after king move"
        assert game.castling_rights_log == [{
            'White': {'kingside': True, 'queenside': True},
            'Black': {'kingside': True, 'queenside': True}
        }]

        game.undo_move()
        assert game.castling_rights[move.piece_moved.color]['kingside'] is True, "Castling rights not restored after undo"
        assert game.castling_rights[move.piece_moved.color]['queenside'] is True, "Castling rights not restored after undo"
        assert game.castling_rights_log == []

    def test_en_passant_logic(self):
        self.setup_method()
        game = self.game

        black_pawn = Pawn("Black", (4, 3))
        game.place_piece_manually(black_pawn, (4, 3))

        white_pawn = game.board[6][4]
        move = Move((6,4), (4,4), game.board)
        game.make_move(move)
        assert game.en_passant_target == (5,4), "En Passant Target square not properly generated"
        assert game.en_passant_target_log == [None], "En Passant Target log not updating correctly"

        en_passant = Move((4,3),(5,4), game.board, is_en_passant=True)
        game.make_move(en_passant)
        assert game.en_passant_target == None, "En Passant Target square not properly cleared"
        assert game.en_passant_target_log == [None, (5,4)], "En Passant Target log not updating correctly"
        assert white_pawn.square == None, "Captured piece's square not updating correctly"
        assert black_pawn.square == (5,4), "Capturing piece's square not updating correctly"
        assert game.board[4][4] == None, "Board does not recognized that piece has been captured"

        game.undo_move()
        assert game.en_passant_target == (5,4), "En Passant Target square not properly restored"
        assert game.en_passant_target_log == [None], "En Passant Target log not restoring correctly"
        assert white_pawn.square == (4,4), "Captured piece's square not restoring correctly"
        assert black_pawn.square == (4,3), "Capturing piece's square not restoring correctly"
        assert game.board[4][4] == white_pawn, "Board does not recognized that piece has been un-captured"

    def test_promotion_and_undo(self):
        empty_game = Gamestate(setup_type="empty")
        
        pawn = Pawn("White", (1, 0))
        empty_game.place_piece_manually(pawn, (1, 0))
        

        move = Move((1, 0), (0, 0), empty_game.board, promote_to="Q")
        empty_game.make_move(move)
        
        assert isinstance(empty_game.board[0][0], Queen), "Promoted piece not generated"
        assert isinstance(empty_game.white_pieces[1], Queen), "Promoted piece not generated"
        assert pawn.square == None, "Pawn not removed from board after promoting"
        assert empty_game.board[1][0] == None, "Pawn not removed from board after promoting"
        
        empty_game.undo_move()
        
        assert isinstance(empty_game.board[1][0], Pawn), "Pawn not restored to board after undo"
        assert len(empty_game.white_pieces) == 1, "Promoted piece not removed after undo"
        assert pawn.square == (1,0), "Pawn not restored to board after un-promoting"
        assert empty_game.board[1][0] == pawn, "Pawn not restored to board after un-promoting"

    def test_castling_out_of_through_check(self):
        empty_game = Gamestate(setup_type="empty")
        
        white_king = King("White", (7, 4))
        white_rook = Rook("White", (7, 7))
        black_king = King("Black", (0, 1)) # King on b8
        empty_game.place_piece_manually(white_king, (7, 4))
        empty_game.place_piece_manually(white_rook, (7, 7))
        empty_game.place_piece_manually(black_king, (0, 1))


        empty_game.castling_rights = {
            #Falsify queenside, otherwise will error since there is no move involving queen's rook
            'White': {'kingside': True, 'queenside': False}, 
            'Black': {'kingside': False, 'queenside': False}
        }
        
        #Can't castle through check
        black_rook = Rook("Black", (0, 5)) # Rook on f8
        empty_game.place_piece_manually(black_rook, (0, 5))

        assert len(empty_game.white_pieces) == 2, "Manually placed pieces not added to piece list"
        assert len(empty_game.black_pieces) == 2, "Manually placed piece not added to piece list"

        assert empty_game.square_under_attack((7, 5)) is True, "Square not under attack when it should be"
        assert empty_game.square_under_attack((7, 4)) is False, "Square under attack when it shouldn't be"
        
        legal_moves = empty_game.get_all_legal_moves()
        
        castle_found = False
        for move in legal_moves:
            if move.start_row == 7 and move.start_col == 4 and move.end_row == 7 and move.end_col == 6:
                castle_found = True
                
        assert not castle_found, "Engine allowed castling through check"

        empty_game.remove_piece_manually((0, 5))
        assert len(empty_game.black_pieces) == 1, "Manually removed piece not removed from piece list"

        #Can't castle out of check
        black_rook = Rook("Black", (0, 4)) # Rook on e8

        empty_game.place_piece_manually(black_rook, (0, 4))

        legal_moves = empty_game.get_all_legal_moves()
        
        castle_found = False
        for move in legal_moves:
            if move.start_row == 7 and move.start_col == 4 and move.end_row == 7 and move.end_col == 6:
                castle_found = True
                
        assert not castle_found, "Engine allowed castling out of check"

        empty_game.remove_piece_manually((0, 4))

        #Can't castle into check
        black_rook = Rook("Black", (0, 6)) # Rook on g8
        empty_game.place_piece_manually(black_rook, (0, 6))

        legal_moves = empty_game.get_all_legal_moves()
        
        castle_found = False
        for move in legal_moves:
            if move.start_row == 7 and move.start_col == 4 and move.end_row == 7 and move.end_col == 6:
                castle_found = True
                
        assert not castle_found, "Engine allowed castling into check"

        empty_game.remove_piece_manually((0, 6))

        #Castling is possible when not in check
        legal_moves = empty_game.get_all_legal_moves()

        castle_found = False
        for move in legal_moves:
            if move.start_row == 7 and move.start_col == 4 and move.end_row == 7 and move.end_col == 6:
                castle_found = True

        assert castle_found, "Engine failed to allow legal castle"

        empty_game.make_move(Move((7,7), (6,7), empty_game.board))
        empty_game.make_move(Move((6,7), (7,7), empty_game.board))

        legal_moves = empty_game.get_all_legal_moves()

        castle_found = False
        for move in legal_moves:
            if move.start_row == 7 and move.start_col == 4 and move.end_row == 7 and move.end_col == 6:
                castle_found = True

        assert not castle_found, "Engine allowed castle after rook had moved"

