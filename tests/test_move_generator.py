import pytest

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
        self.game = GameState(self.board, True, [])

    def test_rook_moves_from_start(self):
        self.setup_method()
        self.board[6][7] = 0
        assert move_generator.get_rook_moves(self.game, self.board, 0, 0) == []
        assert len(move_generator.get_rook_moves(self.game, self.board, 7, 7)) == 6
        moves_for_piece = move_generator.get_rook_moves(self.game, self.board, 7, 7)
        move_list =  []
        move_list.extend(move.get_computer_notation() for move in moves_for_piece)
        assert move_list == ['h1:h2',  'h1:h3', 'h1:h4', 'h1:h5', 'h1:h6', 'h1:h7']
        
    def test_rook_captures(self):
        self.setup_method()
        self.board[0][0] = 'R'
        assert len(move_generator.get_rook_moves(self.game, self.board, 0, 0)) == 2
