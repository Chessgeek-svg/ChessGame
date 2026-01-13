from abc import ABC, abstractmethod
from Move import Move
from typing import List


class Piece(ABC):
    def __init__(self, color, square):
        self.color = color
        self.square = square

    def __str__(self):
        color_code = "w" if self.color == "White" else "b"

        role_map = {
            "Pawn": "p",
            "Rook": "R",
            "Knight": "N",
            "Bishop": "B",
            "Queen": "Q",
            "King": "K",
        }
        role_code = role_map[self.__class__.__name__]

        return color_code + role_code

    def __repr__(self):
        return f"{self.color} {self.__class__.__name__} at {self.square}"

    @abstractmethod
    def get_legal_moves(self, gamestate) -> List["Move"]: ...

    def get_controlled_squares(self, gamestate):
        moves = self.get_legal_moves(gamestate)
        return [(move.end_row, move.end_col) for move in moves]


class SlidingPiece(Piece):
    def _get_sliding_moves(self, gamestate, directions):
        valid_moves = []

        for dr, dc in directions:
            new_r = self.square[0] + dr
            new_c = self.square[1] + dc

            while 0 <= new_r <= 7 and 0 <= new_c <= 7:
                target_square = gamestate.board[new_r][new_c]
                if target_square is None:
                    valid_moves.append(
                        Move(self.square, (new_r, new_c), gamestate.board)
                    )
                elif target_square.color != self.color:
                    valid_moves.append(
                        Move(self.square, (new_r, new_c), gamestate.board)
                    )
                    break
                else:
                    break

                new_r += dr
                new_c += dc

        return valid_moves


class SteppingPiece(Piece):
    def _get_stepping_moves(self, gamestate, directions):
        valid_moves = []

        for dr, dc in directions:
            new_r = self.square[0] + dr
            new_c = self.square[1] + dc

            if 0 <= new_r <= 7 and 0 <= new_c <= 7:
                target_square = gamestate.board[new_r][new_c]
                if target_square is None or target_square.color != self.color:
                    valid_moves.append(
                        Move(self.square, (new_r, new_c), gamestate.board)
                    )

        return valid_moves


class Bishop(SlidingPiece):
    def get_legal_moves(self, gamestate):
        directions = [(-1, -1), (1, -1), (1, 1), (-1, 1)]
        return self._get_sliding_moves(gamestate, directions)


class Rook(SlidingPiece):
    def get_legal_moves(self, gamestate):
        directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]
        return self._get_sliding_moves(gamestate, directions)


class Queen(SlidingPiece):
    def get_legal_moves(self, gamestate):
        directions = [
            (-1, 0),
            (-1, -1),
            (0, -1),
            (1, -1),
            (1, 0),
            (1, 1),
            (0, 1),
            (-1, 1),
        ]
        return self._get_sliding_moves(gamestate, directions)


class Knight(SteppingPiece):
    def get_legal_moves(self, gamestate):
        directions = [
            (-2, -1),
            (-1, -2),
            (1, -2),
            (2, -1),
            (2, 1),
            (1, 2),
            (-1, 2),
            (-2, 1),
        ]
        return self._get_stepping_moves(gamestate, directions)


class King(SteppingPiece):
    def get_legal_moves(self, gamestate):
        directions = [
            (-1, 0),
            (-1, -1),
            (0, -1),
            (1, -1),
            (1, 0),
            (1, 1),
            (0, 1),
            (-1, 1),
        ]
        valid_moves = self._get_stepping_moves(gamestate, directions)
        r, c = self.square

        if (
            gamestate.castling_rights[self.color]["kingside"]
            and gamestate.board[r][c + 1] is None
            and gamestate.board[r][c + 2] is None
        ):
            valid_moves.append(
                Move(self.square, (r, c + 2), gamestate.board, is_castle=True)
            )
        if (
            gamestate.castling_rights[self.color]["queenside"]
            and gamestate.board[r][c - 1] is None
            and gamestate.board[r][c - 2] is None
            and gamestate.board[r][c - 3] is None
        ):
            valid_moves.append(
                Move(self.square, (r, c - 2), gamestate.board, is_castle=True)
            )

        return valid_moves


class Pawn(Piece):
    def get_legal_moves(self, gamestate):
        valid_moves = []

        direction = -1 if self.color == "White" else 1

        r, c = self.square
        target_r = r + direction

        assert 0 <= target_r <= 7, f"Logic Error: Pawn found on illegal rank {r}!"

        if gamestate.board[target_r][c] is None:
            self._add_move_or_promotion_options(
                target_r, c, gamestate.board, valid_moves
            )

            if (r == 1 and self.color == "Black") or (r == 6 and self.color == "White"):
                double_r = r + 2 * direction
                if gamestate.board[double_r][c] is None:
                    self._add_move_or_promotion_options(
                        double_r, c, gamestate.board, valid_moves
                    )

        for dc in [-1, 1]:
            target_c = c + dc
            if 0 <= target_c <= 7:
                target_piece = gamestate.board[target_r][target_c]
                if target_piece and target_piece.color != self.color:
                    self._add_move_or_promotion_options(
                        target_r, target_c, gamestate.board, valid_moves
                    )
                elif (target_r, target_c) == gamestate.en_passant_target:
                    valid_moves.append(
                        Move(
                            self.square,
                            (target_r, target_c),
                            gamestate.board,
                            is_en_passant=True,
                        )
                    )

        return valid_moves

    def get_controlled_squares(self, gamestate):
        attacks = []
        r, c = self.square
        direction = -1 if self.color == "White" else 1
        if 0 <= c - 1 <= 7:
            attacks.append((r + direction, c - 1))
        if 0 <= c + 1 <= 7:
            attacks.append((r + direction, c + 1))

        return attacks

    def _add_move_or_promotion_options(self, end_row, end_col, board, valid_moves):
        promotion_rank = 0 if self.color == "White" else 7

        if end_row == promotion_rank:
            for piece_type in ["N", "R", "B", "Q"]:
                valid_moves.append(
                    Move(self.square, (end_row, end_col), board, promote_to=piece_type)
                )
        else:
            valid_moves.append(Move(self.square, (end_row, end_col), board))
