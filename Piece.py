from abc import ABC, abstractmethod

class Piece(ABC):
    def __init__(self, color, square, previous_square):
        self.color = color
        self.square = square
        self.previous_square = previous_square

    def __repr__(self):
        return f"{self.color} {self.__class__.__name__} at {self.square}"
    
    @abstractmethod
    def get_legal_moves(self, board):
        pass

class SlidingPiece(Piece):
    def _get_sliding_moves(self, board, directions):
        valid_moves = []

        for dr, dc in directions:
            new_r = self.square[0] + dr
            new_c = self.square[1] + dc

            while 0 <= new_r <= 7 and 0 <= new_c <= 7:
                target_square = board[new_r][new_c]
                if target_square is None:
                    valid_moves.append((new_r, new_c))
                elif target_square.color != self.color:
                    valid_moves.append((new_r, new_c))
                    break
                else:
                    break

                new_r += dr
                new_c += dc

        return valid_moves
    
class SteppingPiece(Piece):
    def _get_stepping_moves(self, board, directions):
        valid_moves = []
        
        for dr, dc in directions:
            new_r = self.square[0] + dr
            new_c = self.square[1] + dc

            if 0 <= new_r <= 7 and 0 <= new_c <= 7:
                target_square = board[new_r][new_c]
                if target_square is None or target_square.color != self.color:
                    valid_moves.append((new_r, new_c))

        return(valid_moves)
    
class Bishop(SlidingPiece):
    def get_legal_moves(self, board):
        directions = [(-1,-1), (1,-1), (1,1), (-1,1)]
        return self.get_sliding_moves(board, directions)

class Rook(SlidingPiece):
    def get_legal_moves(self, board):
        directions = [(-1,0), (0,-1), (1,0), (0,1)]
        return self.get_sliding_moves(board, directions)

class Queen(SlidingPiece):
    def get_legal_moves(self, board):
        directions = [(-1,0), (-1,-1), (0,-1), (1,-1), (1,0), (1,1), (0,1), (-1,1)]
        return self.get_sliding_moves(board, directions)
    
class Knight(SteppingPiece):
    def get_legal_moves(self, board):
        directions = [(-2,-1), (-1,-2), (1,-2), (2,-1), (2,1), (1,2), (-1,2), (-2,1)]
        return self._get_stepping_moves(board, directions)
    
class King(SteppingPiece):
    def get_legal_moves(self, board):
        directions = [(-1,0), (-1,-1), (0,-1), (1,-1), (1,0), (1,1), (0,1), (-1,1)]
        return self._get_stepping_moves(board, directions)

class Pawn(Piece):
    def get_legal_moves(self, board):
        valid_moves = []

        direction = -1 if self.color == "White" else 1

        r, c = self.square
        target_r = r + direction

        assert 0 <= target_r <= 7, f"Logic Error: Pawn found on illegal rank {r}!"

        if board[target_r][c] is None:
            valid_moves.append((target_r, c))

            if not self.previous_square:
                double_r = r + 2 * direction
                if board[double_r][c] is None:
                    valid_moves.append((double_r, c))

        for dc in [-1, 1]:
            target_c = c + dc
            if 0 <= target_c <= 7:
                target_piece = board[target_r][target_c]
                if target_piece and target_piece.color != self.color:
                    valid_moves.append((target_r, target_c))

        return valid_moves