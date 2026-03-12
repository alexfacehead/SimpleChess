"""Comprehensive tests for SimpleChess ChessBoard logic."""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from ChessBoard import ChessBoard


def make_empty_board():
    """Create a ChessBoard with an empty board (no pieces)."""
    board = ChessBoard()
    board.board = [[' ' for _ in range(8)] for _ in range(8)]
    return board


# ============================================================
# Basic piece movement tests
# ============================================================

class TestPawnMovement:
    def test_white_pawn_single_forward(self):
        b = ChessBoard()
        assert b.move_piece(1, 0, 2, 0)  # a2 -> a3
        assert b.get_piece(2, 0) == 'P'
        assert b.get_piece(1, 0) == ' '

    def test_white_pawn_double_forward(self):
        b = ChessBoard()
        assert b.move_piece(1, 0, 3, 0)  # a2 -> a4
        assert b.get_piece(3, 0) == 'P'

    def test_white_pawn_double_forward_blocked(self):
        b = ChessBoard()
        b.set_piece(2, 0, 'p')  # Block the path
        assert not b.move_piece(1, 0, 3, 0)

    def test_pawn_cannot_move_backward(self):
        b = make_empty_board()
        b.set_piece(3, 0, 'P')
        b.turn = 'white'
        assert not b.move_piece(3, 0, 2, 0)

    def test_black_pawn_single_forward(self):
        b = ChessBoard()
        b.turn = 'black'
        assert b.move_piece(6, 0, 5, 0)  # a7 -> a6
        assert b.get_piece(5, 0) == 'p'

    def test_black_pawn_double_forward(self):
        b = ChessBoard()
        b.turn = 'black'
        assert b.move_piece(6, 0, 4, 0)

    def test_pawn_cannot_capture_forward(self):
        b = make_empty_board()
        b.set_piece(3, 3, 'P')
        b.set_piece(4, 3, 'p')
        b.turn = 'white'
        assert not b.move_piece(3, 3, 4, 3)

    def test_pawn_diagonal_capture(self):
        b = make_empty_board()
        b.set_piece(0, 4, 'K')
        b.set_piece(7, 4, 'k')
        b.set_piece(3, 3, 'P')
        b.set_piece(4, 4, 'p')
        b.turn = 'white'
        assert b.move_piece(3, 3, 4, 4)
        assert b.get_piece(4, 4) == 'P'
        assert b.get_piece(3, 3) == ' '

    def test_pawn_cannot_capture_own_piece(self):
        b = make_empty_board()
        b.set_piece(3, 3, 'P')
        b.set_piece(4, 4, 'P')
        b.turn = 'white'
        assert not b.move_piece(3, 3, 4, 4)

    def test_pawn_cannot_move_sideways(self):
        b = make_empty_board()
        b.set_piece(3, 3, 'P')
        b.turn = 'white'
        assert not b.move_piece(3, 3, 3, 4)


class TestRookMovement:
    def test_rook_horizontal(self):
        b = make_empty_board()
        b.set_piece(0, 4, 'K')
        b.set_piece(7, 4, 'k')
        b.set_piece(3, 0, 'R')
        b.turn = 'white'
        assert b.move_piece(3, 0, 3, 7)
        assert b.get_piece(3, 7) == 'R'

    def test_rook_vertical(self):
        b = make_empty_board()
        b.set_piece(0, 4, 'K')
        b.set_piece(7, 4, 'k')
        b.set_piece(0, 0, 'R')
        b.turn = 'white'
        assert b.move_piece(0, 0, 7, 0)

    def test_rook_blocked(self):
        b = make_empty_board()
        b.set_piece(0, 0, 'R')
        b.set_piece(0, 3, 'P')
        b.turn = 'white'
        assert not b.move_piece(0, 0, 0, 5)

    def test_rook_cannot_move_diagonally(self):
        b = make_empty_board()
        b.set_piece(0, 0, 'R')
        b.turn = 'white'
        assert not b.move_piece(0, 0, 3, 3)


class TestKnightMovement:
    def test_knight_L_shape(self):
        b = make_empty_board()
        b.set_piece(0, 4, 'K')
        b.set_piece(7, 4, 'k')
        b.set_piece(3, 3, 'N')
        b.turn = 'white'
        # All 8 L-shaped destinations
        valid_dests = [(1, 2), (1, 4), (2, 1), (2, 5), (4, 1), (4, 5), (5, 2), (5, 4)]
        for dx, dy in valid_dests:
            bb = make_empty_board()
            bb.set_piece(0, 4, 'K')
            bb.set_piece(7, 4, 'k')
            bb.set_piece(3, 3, 'N')
            bb.turn = 'white'
            assert bb.move_piece(3, 3, dx, dy), f"Knight should move to ({dx},{dy})"

    def test_knight_invalid_move(self):
        b = make_empty_board()
        b.set_piece(3, 3, 'N')
        b.turn = 'white'
        assert not b.move_piece(3, 3, 4, 4)

    def test_knight_can_jump_over_pieces(self):
        b = ChessBoard()  # Full starting board
        assert b.move_piece(0, 1, 2, 0)  # Knight jumps over pawns


class TestBishopMovement:
    def test_bishop_diagonal(self):
        b = make_empty_board()
        b.set_piece(0, 4, 'K')
        b.set_piece(7, 4, 'k')
        b.set_piece(3, 3, 'B')
        b.turn = 'white'
        assert b.move_piece(3, 3, 6, 6)

    def test_bishop_blocked(self):
        b = make_empty_board()
        b.set_piece(3, 3, 'B')
        b.set_piece(4, 4, 'P')
        b.turn = 'white'
        assert not b.move_piece(3, 3, 5, 5)

    def test_bishop_cannot_move_straight(self):
        b = make_empty_board()
        b.set_piece(3, 3, 'B')
        b.turn = 'white'
        assert not b.move_piece(3, 3, 3, 6)


class TestQueenMovement:
    def test_queen_diagonal(self):
        b = make_empty_board()
        b.set_piece(0, 4, 'K')
        b.set_piece(7, 4, 'k')
        b.set_piece(3, 3, 'Q')
        b.turn = 'white'
        assert b.move_piece(3, 3, 6, 6)

    def test_queen_straight(self):
        b = make_empty_board()
        b.set_piece(0, 4, 'K')
        b.set_piece(7, 4, 'k')
        b.set_piece(3, 3, 'Q')
        b.turn = 'white'
        assert b.move_piece(3, 3, 3, 7)


class TestKingMovement:
    def test_king_one_square(self):
        b = make_empty_board()
        b.set_piece(3, 3, 'K')
        b.set_piece(7, 4, 'k')
        b.turn = 'white'
        assert b.move_piece(3, 3, 4, 3)

    def test_king_cannot_move_two_squares_non_castle(self):
        b = make_empty_board()
        b.set_piece(3, 3, 'K')
        b.set_piece(7, 4, 'k')
        b.turn = 'white'
        # Not a castling position, so 2-square move should fail
        assert not b.move_piece(3, 3, 3, 5)


# ============================================================
# Turn enforcement tests
# ============================================================

class TestTurnEnforcement:
    def test_white_cannot_move_black_piece(self):
        b = ChessBoard()
        assert not b.move_piece(6, 0, 5, 0)  # Try to move black pawn on white's turn

    def test_black_cannot_move_white_piece(self):
        b = ChessBoard()
        b.turn = 'black'
        assert not b.move_piece(1, 0, 2, 0)

    def test_turn_alternates_after_move(self):
        b = ChessBoard()
        assert b.turn == 'white'
        b.move_piece(1, 0, 2, 0)
        assert b.turn == 'black'
        b.move_piece(6, 0, 5, 0)
        assert b.turn == 'white'


# ============================================================
# En passant tests
# ============================================================

class TestEnPassant:
    def test_en_passant_target_set_on_double_push(self):
        b = ChessBoard()
        b.move_piece(1, 4, 3, 4)  # e2 -> e4
        assert b.en_passant_target == (2, 4)

    def test_en_passant_target_cleared_on_other_move(self):
        b = ChessBoard()
        b.move_piece(1, 4, 3, 4)  # e2 -> e4
        b.move_piece(6, 0, 5, 0)  # a7 -> a6
        assert b.en_passant_target is None

    def test_white_en_passant_capture(self):
        b = make_empty_board()
        b.set_piece(0, 4, 'K')
        b.set_piece(7, 4, 'k')
        # White pawn at e5 (row 4, col 4), black pawn about to double-push d7->d5
        b.set_piece(4, 4, 'P')
        b.set_piece(6, 3, 'p')
        b.turn = 'black'
        b.move_piece(6, 3, 4, 3)  # d7 -> d5 (double push)
        assert b.en_passant_target == (5, 3)

        # White captures en passant: e5 x d6
        assert b.move_piece(4, 4, 5, 3)
        assert b.get_piece(5, 3) == 'P'  # White pawn moved to d6
        assert b.get_piece(4, 3) == ' '  # Black pawn captured
        assert b.get_piece(4, 4) == ' '  # Original square cleared

    def test_black_en_passant_capture(self):
        b = make_empty_board()
        b.set_piece(0, 4, 'K')
        b.set_piece(7, 4, 'k')
        b.set_piece(3, 3, 'p')  # Black pawn at d4
        b.set_piece(1, 4, 'P')  # White pawn at e2
        b.turn = 'white'
        b.move_piece(1, 4, 3, 4)  # e2 -> e4 (double push)
        assert b.en_passant_target == (2, 4)

        # Black captures en passant: d4 x e3
        assert b.move_piece(3, 3, 2, 4)
        assert b.get_piece(2, 4) == 'p'
        assert b.get_piece(3, 4) == ' '  # White pawn captured

    def test_en_passant_only_available_immediately(self):
        b = make_empty_board()
        b.set_piece(0, 4, 'K')
        b.set_piece(7, 4, 'k')
        b.set_piece(4, 4, 'P')
        b.set_piece(6, 3, 'p')
        b.set_piece(1, 0, 'P')  # Extra pawn for tempo
        b.set_piece(6, 7, 'p')  # Extra pawn for tempo
        b.turn = 'black'
        b.move_piece(6, 3, 4, 3)  # d7 -> d5

        # White plays something else
        b.move_piece(1, 0, 2, 0)  # a2 -> a3
        # Black plays something
        b.move_piece(6, 7, 5, 7)  # h7 -> h6

        # Now white tries en passant — too late, should fail
        assert not b.move_piece(4, 4, 5, 3)

    def test_en_passant_score_tracking(self):
        b = make_empty_board()
        b.set_piece(0, 4, 'K')
        b.set_piece(7, 4, 'k')
        b.set_piece(4, 4, 'P')
        b.set_piece(6, 3, 'p')
        b.turn = 'black'
        b.move_piece(6, 3, 4, 3)
        b.move_piece(4, 4, 5, 3)  # En passant capture
        assert b.score['white'] == 1  # Captured a pawn worth 1

    def test_en_passant_undo(self):
        b = make_empty_board()
        b.set_piece(0, 4, 'K')
        b.set_piece(7, 4, 'k')
        b.set_piece(4, 4, 'P')
        b.set_piece(6, 3, 'p')
        b.turn = 'black'
        b.move_piece(6, 3, 4, 3)
        b.move_piece(4, 4, 5, 3)  # En passant

        b.undo_move()
        assert b.get_piece(4, 4) == 'P'  # White pawn back
        assert b.get_piece(4, 3) == 'p'  # Black pawn restored
        assert b.get_piece(5, 3) == ' '  # Destination cleared
        assert b.score['white'] == 0


# ============================================================
# Castling tests
# ============================================================

class TestCastling:
    def _setup_kingside_castle(self, color='white'):
        b = make_empty_board()
        if color == 'white':
            b.set_piece(0, 4, 'K')
            b.set_piece(0, 7, 'R')
            b.set_piece(7, 4, 'k')
            b.turn = 'white'
        else:
            b.set_piece(7, 4, 'k')
            b.set_piece(7, 7, 'r')
            b.set_piece(0, 4, 'K')
            b.turn = 'black'
        return b

    def _setup_queenside_castle(self, color='white'):
        b = make_empty_board()
        if color == 'white':
            b.set_piece(0, 4, 'K')
            b.set_piece(0, 0, 'R')
            b.set_piece(7, 4, 'k')
            b.turn = 'white'
        else:
            b.set_piece(7, 4, 'k')
            b.set_piece(7, 0, 'r')
            b.set_piece(0, 4, 'K')
            b.turn = 'black'
        return b

    def test_white_kingside_castle(self):
        b = self._setup_kingside_castle('white')
        assert b.move_piece(0, 4, 0, 6)  # King to g1
        assert b.get_piece(0, 6) == 'K'
        assert b.get_piece(0, 5) == 'R'
        assert b.get_piece(0, 4) == ' '
        assert b.get_piece(0, 7) == ' '

    def test_white_queenside_castle(self):
        b = self._setup_queenside_castle('white')
        assert b.move_piece(0, 4, 0, 2)  # King to c1
        assert b.get_piece(0, 2) == 'K'
        assert b.get_piece(0, 3) == 'R'
        assert b.get_piece(0, 4) == ' '
        assert b.get_piece(0, 0) == ' '

    def test_black_kingside_castle(self):
        b = self._setup_kingside_castle('black')
        assert b.move_piece(7, 4, 7, 6)
        assert b.get_piece(7, 6) == 'k'
        assert b.get_piece(7, 5) == 'r'

    def test_black_queenside_castle(self):
        b = self._setup_queenside_castle('black')
        assert b.move_piece(7, 4, 7, 2)
        assert b.get_piece(7, 2) == 'k'
        assert b.get_piece(7, 3) == 'r'

    def test_castle_blocked_by_king_moved(self):
        b = self._setup_kingside_castle('white')
        b.king_moved['white'] = True
        assert not b.move_piece(0, 4, 0, 6)

    def test_castle_blocked_by_rook_moved(self):
        b = self._setup_kingside_castle('white')
        b.king_rook_moved['white'] = True
        assert not b.move_piece(0, 4, 0, 6)

    def test_castle_blocked_by_piece_in_path(self):
        b = self._setup_kingside_castle('white')
        b.set_piece(0, 5, 'B')
        assert not b.move_piece(0, 4, 0, 6)

    def test_castle_blocked_when_in_check(self):
        b = self._setup_kingside_castle('white')
        b.set_piece(4, 4, 'r')  # Black rook attacks king
        assert not b.move_piece(0, 4, 0, 6)

    def test_castle_blocked_when_passing_through_check(self):
        b = self._setup_kingside_castle('white')
        b.set_piece(4, 5, 'r')  # Black rook attacks f1
        assert not b.move_piece(0, 4, 0, 6)

    def test_castle_blocked_when_landing_in_check(self):
        b = self._setup_kingside_castle('white')
        b.set_piece(4, 6, 'r')  # Black rook attacks g1
        assert not b.move_piece(0, 4, 0, 6)

    def test_castle_undo_kingside(self):
        b = self._setup_kingside_castle('white')
        b.move_piece(0, 4, 0, 6)
        b.undo_move()
        assert b.get_piece(0, 4) == 'K'
        assert b.get_piece(0, 7) == 'R'
        assert b.get_piece(0, 6) == ' '
        assert b.get_piece(0, 5) == ' '
        assert not b.king_moved['white']
        assert not b.king_rook_moved['white']

    def test_castle_undo_queenside(self):
        b = self._setup_queenside_castle('white')
        b.move_piece(0, 4, 0, 2)
        b.undo_move()
        assert b.get_piece(0, 4) == 'K'
        assert b.get_piece(0, 0) == 'R'
        assert b.get_piece(0, 2) == ' '
        assert b.get_piece(0, 3) == ' '
        assert not b.king_moved['white']
        assert not b.queen_rook_moved['white']

    def test_castle_no_rook(self):
        b = make_empty_board()
        b.set_piece(0, 4, 'K')
        b.set_piece(7, 4, 'k')
        b.turn = 'white'
        assert not b.move_piece(0, 4, 0, 6)


# ============================================================
# Pawn promotion tests
# ============================================================

class TestPawnPromotion:
    def test_white_pawn_promotes_to_queen(self):
        b = make_empty_board()
        b.set_piece(0, 4, 'K')
        b.set_piece(7, 4, 'k')
        b.set_piece(6, 0, 'P')
        b.turn = 'white'
        assert b.move_piece(6, 0, 7, 0)
        assert b.get_piece(7, 0) == 'Q'

    def test_black_pawn_promotes_to_queen(self):
        b = make_empty_board()
        b.set_piece(0, 4, 'K')
        b.set_piece(7, 4, 'k')
        b.set_piece(1, 0, 'p')
        b.turn = 'black'
        assert b.move_piece(1, 0, 0, 0)
        assert b.get_piece(0, 0) == 'q'

    def test_promotion_with_capture(self):
        b = make_empty_board()
        b.set_piece(0, 4, 'K')
        b.set_piece(7, 4, 'k')
        b.set_piece(6, 0, 'P')
        b.set_piece(7, 1, 'r')
        b.turn = 'white'
        assert b.move_piece(6, 0, 7, 1)
        assert b.get_piece(7, 1) == 'Q'
        assert b.score['white'] == 5  # Captured rook


# ============================================================
# Check, checkmate, stalemate tests
# ============================================================

class TestCheck:
    def test_basic_check_detection(self):
        b = make_empty_board()
        b.set_piece(0, 4, 'K')
        b.set_piece(7, 4, 'k')
        b.set_piece(4, 4, 'r')  # Black rook on e5 attacking white king on e1
        assert b.is_in_check('white')
        assert not b.is_in_check('black')

    def test_cannot_move_into_check(self):
        b = make_empty_board()
        b.set_piece(0, 4, 'K')
        b.set_piece(7, 4, 'k')
        b.set_piece(3, 3, 'r')  # Black rook attacks d-file and rank 4
        b.turn = 'white'
        # King tries to move to d1 which is attacked by rook
        assert not b.move_piece(0, 4, 0, 3)

    def test_must_escape_check(self):
        b = make_empty_board()
        b.set_piece(0, 4, 'K')
        b.set_piece(7, 4, 'k')
        b.set_piece(0, 0, 'R')  # White rook
        b.set_piece(4, 4, 'r')  # Black rook giving check
        b.turn = 'white'
        # Try to move rook instead of escaping check
        assert not b.move_piece(0, 0, 0, 1)

    def test_game_status_check(self):
        b = make_empty_board()
        b.set_piece(0, 4, 'K')
        b.set_piece(7, 4, 'k')
        b.set_piece(1, 0, 'P')
        b.set_piece(6, 3, 'r')
        b.turn = 'black'
        b.move_piece(6, 3, 0, 3)  # Rook to d1, checking white king
        # After this move, it's white's turn and white is in check
        assert b.game_status == 'check'


class TestCheckmate:
    def test_scholars_mate(self):
        """Test a basic back-rank checkmate."""
        b = make_empty_board()
        b.set_piece(0, 4, 'K')
        b.set_piece(7, 4, 'k')
        # Black queen and rook deliver checkmate
        b.set_piece(0, 0, 'q')  # Queen on a1
        b.set_piece(1, 7, 'r')  # Rook on h2 — king has no escape
        b.turn = 'white'
        b.update_game_status()
        assert b.game_status == 'checkmate'

    def test_back_rank_mate(self):
        b = make_empty_board()
        b.set_piece(0, 6, 'K')  # King on g1
        b.set_piece(1, 5, 'P')  # Pawns blocking escape
        b.set_piece(1, 6, 'P')
        b.set_piece(1, 7, 'P')
        b.set_piece(7, 4, 'k')
        b.set_piece(0, 0, 'r')  # Black rook delivers back rank mate
        b.turn = 'white'
        b.update_game_status()
        assert b.game_status == 'checkmate'


class TestStalemate:
    def test_king_stalemated(self):
        b = make_empty_board()
        b.set_piece(0, 0, 'K')
        b.set_piece(7, 7, 'k')
        b.set_piece(1, 2, 'q')  # Blocks a2, b2
        b.set_piece(2, 1, 'r')  # Blocks b-file and row 3
        b.turn = 'white'
        b.update_game_status()
        assert b.game_status == 'stalemate'


# ============================================================
# Undo tests
# ============================================================

class TestUndo:
    def test_undo_simple_move(self):
        b = ChessBoard()
        b.move_piece(1, 4, 3, 4)  # e2->e4
        b.undo_move()
        assert b.get_piece(1, 4) == 'P'
        assert b.get_piece(3, 4) == ' '
        assert b.turn == 'white'

    def test_undo_capture(self):
        b = make_empty_board()
        b.set_piece(0, 4, 'K')
        b.set_piece(7, 4, 'k')
        b.set_piece(3, 3, 'P')
        b.set_piece(4, 4, 'p')
        b.turn = 'white'
        b.move_piece(3, 3, 4, 4)
        b.undo_move()
        assert b.get_piece(3, 3) == 'P'
        assert b.get_piece(4, 4) == 'p'
        assert b.score['white'] == 0

    def test_undo_empty_history(self):
        b = ChessBoard()
        assert not b.undo_move()

    def test_multiple_undo(self):
        b = ChessBoard()
        b.move_piece(1, 4, 3, 4)  # e2->e4
        b.move_piece(6, 4, 4, 4)  # e7->e5
        b.undo_move()
        b.undo_move()
        assert b.get_piece(1, 4) == 'P'
        assert b.get_piece(6, 4) == 'p'
        assert b.turn == 'white'


# ============================================================
# Score tracking tests
# ============================================================

class TestScoring:
    def test_capture_updates_score(self):
        b = make_empty_board()
        b.set_piece(0, 4, 'K')
        b.set_piece(7, 4, 'k')
        b.set_piece(3, 3, 'Q')
        b.set_piece(4, 4, 'r')
        b.turn = 'white'
        b.move_piece(3, 3, 4, 4)
        assert b.score['white'] == 5  # Rook = 5 points

    def test_score_undo(self):
        b = make_empty_board()
        b.set_piece(0, 4, 'K')
        b.set_piece(7, 4, 'k')
        b.set_piece(3, 3, 'Q')
        b.set_piece(4, 4, 'r')
        b.turn = 'white'
        b.move_piece(3, 3, 4, 4)
        b.undo_move()
        assert b.score['white'] == 0


# ============================================================
# Board validity tests
# ============================================================

class TestBoardValidity:
    def test_valid_starting_board(self):
        b = ChessBoard()
        assert b.is_valid()

    def test_invalid_no_kings(self):
        b = make_empty_board()
        assert not b.is_valid()

    def test_invalid_two_white_kings(self):
        b = make_empty_board()
        b.set_piece(0, 0, 'K')
        b.set_piece(0, 7, 'K')
        b.set_piece(7, 0, 'k')
        assert not b.is_valid()


# ============================================================
# Castling rights tracking tests
# ============================================================

class TestCastlingRights:
    def test_king_move_loses_castling_rights(self):
        b = make_empty_board()
        b.set_piece(0, 4, 'K')
        b.set_piece(0, 7, 'R')
        b.set_piece(0, 0, 'R')
        b.set_piece(7, 4, 'k')
        b.turn = 'white'
        b.move_piece(0, 4, 0, 3)  # King moves
        assert b.king_moved['white']

    def test_rook_move_loses_castling_rights(self):
        b = make_empty_board()
        b.set_piece(0, 4, 'K')
        b.set_piece(0, 7, 'R')
        b.set_piece(7, 4, 'k')
        b.turn = 'white'
        b.move_piece(0, 7, 0, 6)  # Kingside rook moves
        assert b.king_rook_moved['white']


# ============================================================
# Pinned piece tests
# ============================================================

class TestPinnedPieces:
    def test_pinned_piece_cannot_move(self):
        """A piece pinned to the king cannot move away from the pin line."""
        b = make_empty_board()
        b.set_piece(0, 0, 'K')
        b.set_piece(7, 4, 'k')
        b.set_piece(0, 3, 'R')  # White rook on d1
        b.set_piece(0, 5, 'r')  # Black rook pins nothing in this setup
        # Better pin setup: king on e1, bishop on d2, black rook on c3
        b2 = make_empty_board()
        b2.set_piece(0, 4, 'K')  # King on e1
        b2.set_piece(1, 3, 'B')  # Bishop on d2 (diagonal from king)
        b2.set_piece(7, 4, 'k')
        b2.set_piece(4, 0, 'r')  # Black rook on a5 — pins nothing
        # Pin: King e1, Bishop d2, Black queen a5 on same diagonal
        b3 = make_empty_board()
        b3.set_piece(0, 4, 'K')  # King on e1
        b3.set_piece(1, 3, 'N')  # Knight on d2
        b3.set_piece(7, 7, 'k')
        b3.set_piece(5, 4, 'r')  # Black rook on e6 — attacks along e-file
        b3.turn = 'white'
        # Knight is not on e-file so not pinned, but let's test a real pin
        b4 = make_empty_board()
        b4.set_piece(0, 4, 'K')  # King e1
        b4.set_piece(3, 4, 'R')  # White rook on e4 (same file as king)
        b4.set_piece(7, 4, 'k')
        b4.set_piece(6, 4, 'r')  # Black rook on e7 attacks along e-file
        b4.turn = 'white'
        # Rook is pinned to king along e-file, cannot move off e-file
        assert not b4.move_piece(3, 4, 3, 5)  # Rook tries to move sideways
        # But can move along the pin line
        assert b4.move_piece(3, 4, 5, 4)  # Rook moves forward on e-file


if __name__ == '__main__':
    import pytest
    pytest.main([__file__, '-v'])
