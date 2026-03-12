class ChessBoard:
    def __init__(self):
        self.piece_values = {'p': 1, 'r': 5, 'n': 3, 'b': 3, 'q': 9, 'k': 0}
        self.score = {'white': 0, 'black': 0}
        self.turn = 'white'
        
        self.move_history = []
        self.board = [[' ' for _ in range(8)] for _ in range(8)]
        self.initialize_board()

        # Castling constituents' has_moved status tracking
        self.king_rook_moved = {'white': False, 'black': False}
        self.queen_rook_moved = {'white': False, 'black': False}
        self.king_moved = {'white': False, 'black': False}

        # En passant target square (row, col) — set when a pawn moves 2 squares
        self.en_passant_target = None

        # Game status
        self.game_status = 'active'  # 'active', 'check', 'checkmate', 'stalemate'

    # Return score
    def get_score(self):
        return self.score

    @staticmethod
    def get_pos(x, y):
        pos_map = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}
        return pos_map[y] + str(8 - x)

    def initialize_board(self):
        pieces = ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']

        for i, piece in enumerate(pieces):
            self.board[0][i] = piece.lower()
            self.board[7][i] = piece

        for i in range(8):
            self.board[1][i] = 'p'
            self.board[6][i] = 'P'

    def get_piece(self, x, y):
        return self.board[x][y]

    def set_piece(self, x, y, piece):
        self.board[x][y] = piece

    def move_piece(self, start_x, start_y, dest_x, dest_y):
        piece = self.get_piece(start_x, start_y)
        destination_piece = self.get_piece(dest_x, dest_y)
        if (piece.isupper() and self.turn == 'black') or (piece.islower() and self.turn == 'white'):
            return False

        # Detect castling: king moves exactly 2 squares horizontally
        is_castle_move = piece.lower() == "k" and abs(dest_y - start_y) == 2 and start_x == dest_x
        if not is_castle_move and destination_piece != ' ' and piece.islower() == destination_piece.islower():
            return False

        is_valid_move = False

        piece_type = piece.lower()
        valid_move_methods = {
            'r': self.valid_rook_move,
            'n': self.valid_knight_move,
            'b': self.valid_bishop_move,
            'q': self.valid_queen_move,
            'k': self.valid_king_move,
            'p': self.valid_pawn_move
        }

        if is_castle_move:
            is_valid_move = self.handle_castling_conditions(start_x, start_y, dest_x, dest_y)
        elif piece_type in valid_move_methods:
            is_valid_move = valid_move_methods[piece_type](start_x, start_y, dest_x, dest_y)

        if not is_valid_move:
            return False

        if is_castle_move:
            # Castling is fully handled inside handle_castling_conditions
            self.move_history.append(((start_x, start_y), (dest_x, dest_y), piece, ' ', 0, 'castle'))
            self.turn = 'black' if self.turn == 'white' else 'white'
            self.update_game_status()
            return True

        # Check if this move would leave own king in check
        if not self._is_legal_move(start_x, start_y, dest_x, dest_y):
            return False

        score_gain = 0
        en_passant_captured = None

        # En passant capture
        if piece_type == 'p' and abs(dest_y - start_y) == 1 and destination_piece == ' ':
            en_passant_captured = (start_x, dest_y)
            captured_piece = self.get_piece(start_x, dest_y)
            score_gain = self.piece_values['p']
            if captured_piece.islower():
                self.score['white'] += score_gain
            else:
                self.score['black'] += score_gain
            self.set_piece(start_x, dest_y, ' ')
        elif destination_piece != ' ':
            score_gain = self.piece_values[destination_piece.lower()]
            if destination_piece.islower():
                self.score['white'] += score_gain
            else:
                self.score['black'] += score_gain

        self.set_piece(dest_x, dest_y, piece)
        self.set_piece(start_x, start_y, ' ')

        # Handle pawn promotion
        if piece_type == 'p':
            if (piece.isupper() and dest_x == 0) or (piece.islower() and dest_x == 7):
                self.do_pawn_promotion(dest_x, dest_y, piece)

        # Track en passant eligibility: pawn moved 2 squares
        if piece_type == 'p' and abs(dest_x - start_x) == 2:
            self.en_passant_target = ((start_x + dest_x) // 2, start_y)
        else:
            self.en_passant_target = None

        move_tag = 'en_passant' if en_passant_captured else 'normal'
        self.move_history.append(((start_x, start_y), (dest_x, dest_y), piece, destination_piece, score_gain, move_tag))

        # Track rook/king movement for castling rights
        color = self.turn  # Turn hasn't swapped yet
        if piece_type == "k":
            self.king_moved[color] = True
        elif piece_type == "r":
            home_row = 7 if color == 'white' else 0
            if start_x == home_row:
                if start_y == 0:
                    self.queen_rook_moved[color] = True
                elif start_y == 7:
                    self.king_rook_moved[color] = True

        self.turn = 'black' if self.turn == 'white' else 'white'
        self.update_game_status()
        return True

    def get_history(self):
        return str(self.move_history)

    def is_valid(self):
        """
        Check if the current board state is valid.
        For simplicity, this function will only check if there is exactly one king for each side.
        """
        white_king_count = 0
        black_king_count = 0

        for row in range(8):
            for col in range(8):
                piece = self.get_piece(row, col)
                if piece == 'K':
                    white_king_count += 1
                elif piece == 'k':
                    black_king_count += 1

        return white_king_count == 1 and black_king_count == 1

    def handle_castling_conditions(self, start_x, start_y, dest_x, dest_y):
        """Validate and perform castling. King moves 2 squares toward rook."""
        piece = self.get_piece(start_x, start_y)
        color = 'white' if piece.isupper() else 'black'

        if self.king_moved[color]:
            return False

        # Determine direction: kingside (right) or queenside (left)
        is_kingside = dest_y > start_y
        rook_y = 7 if is_kingside else 0

        # Check the relevant rook hasn't moved
        if is_kingside and self.king_rook_moved[color]:
            return False
        if not is_kingside and self.queen_rook_moved[color]:
            return False

        # Check rook is actually there
        rook = self.get_piece(start_x, rook_y)
        if rook.lower() != 'r' or (rook.isupper() != piece.isupper()):
            return False

        # Check path between king and rook is clear
        step = 1 if rook_y > start_y else -1
        for y in range(start_y + step, rook_y, step):
            if self.get_piece(start_x, y) != ' ':
                return False

        # King must not be in check, pass through check, or land in check
        opponent_turn = 'black' if color == 'white' else 'white'
        king_path = [start_y, start_y + step, dest_y]
        for y in king_path:
            if self.check_if_in_check(start_x, y, opponent_turn):
                return False

        # Perform the castle
        self.perform_castle(start_x, start_y, rook_y, is_kingside)
        return True
    

    def check_if_in_check(self, king_x, king_y, attacker_color):
        """Check if the square (king_x, king_y) is attacked by pieces of attacker_color."""
        attacker_is_upper = (attacker_color == 'white')
        for x in range(8):
            for y in range(8):
                piece = self.get_piece(x, y)
                if piece != ' ' and piece.isupper() == attacker_is_upper:
                    piece_type = piece.lower()
                    if piece_type == 'p':
                        # Pawns attack diagonally — check manually to avoid move-vs-capture confusion
                        direction = -1 if piece.isupper() else 1
                        if x + direction == king_x and abs(y - king_y) == 1:
                            return True
                    else:
                        valid_move_methods = {
                            'r': self.valid_rook_move,
                            'n': self.valid_knight_move,
                            'b': self.valid_bishop_move,
                            'q': self.valid_queen_move,
                            'k': self.valid_king_move,
                        }
                        if piece_type in valid_move_methods:
                            if valid_move_methods[piece_type](x, y, king_x, king_y):
                                return True
        return False

    def perform_castle(self, king_x, king_y, rook_y, is_kingside):
        """Move king 2 squares toward rook, place rook on other side of king."""
        king = self.get_piece(king_x, king_y)
        rook = self.get_piece(king_x, rook_y)
        color = 'white' if king.isupper() else 'black'

        king_dest_y = king_y + 2 if is_kingside else king_y - 2
        rook_dest_y = king_dest_y - 1 if is_kingside else king_dest_y + 1

        # Clear original positions
        self.set_piece(king_x, king_y, ' ')
        self.set_piece(king_x, rook_y, ' ')

        # Place pieces at new positions
        self.set_piece(king_x, king_dest_y, king)
        self.set_piece(king_x, rook_dest_y, rook)

        # Update castling flags
        self.king_moved[color] = True
        if is_kingside:
            self.king_rook_moved[color] = True
        else:
            self.queen_rook_moved[color] = True

    def undo_move(self, is_recursive=False):
        if not self.move_history:
            return False

        last_move = self.move_history.pop()
        (start_x, start_y), (dest_x, dest_y), moved_piece, destination_piece, score_change, move_tag = last_move

        if move_tag == 'castle':
            color = 'white' if moved_piece.isupper() else 'black'
            is_kingside = dest_y > start_y
            rook_char = 'R' if moved_piece == 'K' else 'r'

            # King was at start_y, moved to dest_y (2 squares)
            # Rook was at 7 (kingside) or 0 (queenside), moved next to king
            king_dest_y = dest_y
            rook_dest_y = dest_y - 1 if is_kingside else dest_y + 1
            rook_orig_y = 7 if is_kingside else 0

            # Clear castled positions
            self.set_piece(start_x, king_dest_y, ' ')
            self.set_piece(start_x, rook_dest_y, ' ')

            # Restore original positions
            self.set_piece(start_x, start_y, moved_piece)
            self.set_piece(start_x, rook_orig_y, rook_char)

            # Reset castling flags
            self.king_moved[color] = False
            if is_kingside:
                self.king_rook_moved[color] = False
            else:
                self.queen_rook_moved[color] = False

        elif move_tag == 'en_passant':
            # Restore moving pawn to original position
            self.set_piece(start_x, start_y, moved_piece)
            self.set_piece(dest_x, dest_y, ' ')

            # Restore captured pawn (it was on same row as moving pawn, same col as destination)
            captured_pawn = 'p' if moved_piece.isupper() else 'P'
            self.set_piece(start_x, dest_y, captured_pawn)

            # Reverse score
            if score_change != 0:
                if moved_piece.isupper():
                    self.score['white'] -= score_change
                else:
                    self.score['black'] -= score_change

        else:
            # Normal move
            self.set_piece(start_x, start_y, moved_piece)
            self.set_piece(dest_x, dest_y, destination_piece)

            if score_change != 0:
                if moved_piece.isupper():
                    self.score['white'] -= score_change
                else:
                    self.score['black'] -= score_change

        # Restore en passant target from the move before this one
        if self.move_history:
            prev_move = self.move_history[-1]
            prev_piece = prev_move[2]
            prev_start_x = prev_move[0][0]
            prev_dest_x = prev_move[1][0]
            if prev_piece.lower() == 'p' and abs(prev_dest_x - prev_start_x) == 2:
                self.en_passant_target = ((prev_start_x + prev_dest_x) // 2, prev_move[0][1])
            else:
                self.en_passant_target = None
        else:
            self.en_passant_target = None

        # Swap turn back
        self.turn = 'black' if self.turn == 'white' else 'white'
        self.update_game_status()
        return True

    def print_board(self):
        for row in self.board:
            print(' '.join(row))

    def valid_bishop_move(self, start_x, start_y, dest_x, dest_y):
        if abs(dest_x - start_x) != abs(dest_y - start_y):
            return False

        x_step = 1 if dest_x > start_x else -1
        y_step = 1 if dest_y > start_y else -1

        x, y = start_x + x_step, start_y + y_step

        while x != dest_x and y != dest_y:
            if self.get_piece(x, y) != ' ':
                return False
            x += x_step
            y += y_step

        return True

    def do_pawn_promotion(self, dest_x, dest_y, piece):
        """Promote pawn to queen. Piece is already placed at dest; just convert it."""
        converted_piece = 'Q' if piece.isupper() else 'q'
        self.set_piece(dest_x, dest_y, converted_piece)
    
    def is_pawn_starting_position(self, x, is_white):
        return (x == 6 and is_white) or (x == 1 and not is_white)

    def valid_pawn_move(self, start_x, start_y, dest_x, dest_y):
        piece = self.get_piece(start_x, start_y)
        is_white = piece.isupper()
        direction = -1 if is_white else 1
        dest_piece = self.get_piece(dest_x, dest_y)

        # Must move exactly one rank forward (or two from start)
        if dest_x != start_x + direction and dest_x != start_x + 2 * direction:
            return False

        # Straight moves
        if dest_y == start_y:
            if dest_piece != ' ':
                return False
            if dest_x == start_x + direction:
                return True
            if dest_x == start_x + 2 * direction and self.is_pawn_starting_position(start_x, is_white):
                return self.get_piece(start_x + direction, start_y) == ' '
            return False

        # Diagonal captures (including en passant)
        if abs(dest_y - start_y) == 1 and dest_x == start_x + direction:
            # Normal diagonal capture
            if dest_piece != ' ' and dest_piece.isupper() != is_white:
                return True
            # En passant capture
            if self.en_passant_target and (dest_x, dest_y) == self.en_passant_target:
                return True

        return False

    def valid_king_move(self, start_x, start_y, dest_x, dest_y):
        x_diff = abs(start_x - dest_x)
        y_diff = abs(start_y - dest_y)
        return x_diff <= 1 and y_diff <= 1 and (x_diff + y_diff) > 0

    def valid_queen_move(self, start_x, start_y, dest_x, dest_y):
        return self.valid_rook_move(start_x, start_y, dest_x, dest_y) or self.valid_bishop_move(start_x, start_y, dest_x, dest_y)

    def valid_rook_move(self, start_x, start_y, dest_x, dest_y):
        if start_x != dest_x and start_y != dest_y:
            return False

        if start_x == dest_x:
            step = 1 if dest_y > start_y else -1
            for y in range(start_y + step, dest_y, step):
                if self.get_piece(start_x, y) != ' ':
                    return False
        else:
            step = 1 if dest_x > start_x else -1
            for x in range(start_x + step, dest_x, step):
                if self.get_piece(x, start_y) != ' ':
                    return False

        return True

    def valid_knight_move(self, start_x, start_y, dest_x, dest_y):
        x_diff = abs(start_x - dest_x)
        y_diff = abs(start_y - dest_y)
        return (x_diff == 2 and y_diff == 1) or (x_diff == 1 and y_diff == 2)

    def is_space_empty(self, x, y):
        return self.get_piece(x, y) == ' '

    def find_king(self, color):
        """Find the king's position for the given color."""
        king_char = 'K' if color == 'white' else 'k'
        for x in range(8):
            for y in range(8):
                if self.get_piece(x, y) == king_char:
                    return (x, y)
        return None

    def is_in_check(self, color):
        """Check if the given color's king is in check."""
        king_pos = self.find_king(color)
        if not king_pos:
            return False
        attacker = 'black' if color == 'white' else 'white'
        return self.check_if_in_check(king_pos[0], king_pos[1], attacker)

    def has_legal_moves(self, color):
        """Check if the given color has any legal move (move that doesn't leave king in check)."""
        is_upper = (color == 'white')
        for x in range(8):
            for y in range(8):
                piece = self.get_piece(x, y)
                if piece == ' ' or piece.isupper() != is_upper:
                    continue
                for dx in range(8):
                    for dy in range(8):
                        if x == dx and y == dy:
                            continue
                        # Try the move temporarily
                        if self._is_legal_move(x, y, dx, dy):
                            return True
        return False

    def _is_legal_move(self, start_x, start_y, dest_x, dest_y):
        """Check if a move is legal (valid + doesn't leave own king in check)."""
        piece = self.get_piece(start_x, start_y)
        dest_piece = self.get_piece(dest_x, dest_y)
        if piece == ' ':
            return False

        color = 'white' if piece.isupper() else 'black'

        # Can't capture own pieces
        if dest_piece != ' ' and dest_piece.isupper() == piece.isupper():
            return False

        piece_type = piece.lower()

        # Check castling
        if piece_type == 'k' and abs(dest_y - start_y) == 2 and start_x == dest_x:
            # Castling validity is fully checked in handle_castling_conditions
            # We need to simulate it
            return self._test_castle_legal(start_x, start_y, dest_x, dest_y)

        # Check basic move validity
        valid_move_methods = {
            'r': self.valid_rook_move,
            'n': self.valid_knight_move,
            'b': self.valid_bishop_move,
            'q': self.valid_queen_move,
            'k': self.valid_king_move,
            'p': self.valid_pawn_move
        }

        if piece_type not in valid_move_methods:
            return False
        if not valid_move_methods[piece_type](start_x, start_y, dest_x, dest_y):
            return False

        # Simulate the move and check if own king is in check
        # Handle en passant capture
        en_passant_captured_pos = None
        en_passant_captured_piece = None
        if piece_type == 'p' and abs(dest_y - start_y) == 1 and dest_piece == ' ':
            if self.en_passant_target and (dest_x, dest_y) == self.en_passant_target:
                en_passant_captured_pos = (start_x, dest_y)
                en_passant_captured_piece = self.get_piece(start_x, dest_y)
                self.set_piece(start_x, dest_y, ' ')

        self.set_piece(dest_x, dest_y, piece)
        self.set_piece(start_x, start_y, ' ')

        attacker = 'black' if color == 'white' else 'white'
        king_pos = self.find_king(color)
        in_check = king_pos is not None and self.check_if_in_check(king_pos[0], king_pos[1], attacker)

        # Undo simulation
        self.set_piece(start_x, start_y, piece)
        self.set_piece(dest_x, dest_y, dest_piece)
        if en_passant_captured_pos:
            self.set_piece(en_passant_captured_pos[0], en_passant_captured_pos[1], en_passant_captured_piece)

        return not in_check

    def _test_castle_legal(self, start_x, start_y, dest_x, dest_y):
        """Test if castling is legal without performing it."""
        piece = self.get_piece(start_x, start_y)
        color = 'white' if piece.isupper() else 'black'

        if self.king_moved[color]:
            return False

        is_kingside = dest_y > start_y
        rook_y = 7 if is_kingside else 0

        if is_kingside and self.king_rook_moved[color]:
            return False
        if not is_kingside and self.queen_rook_moved[color]:
            return False

        rook = self.get_piece(start_x, rook_y)
        if rook.lower() != 'r' or (rook.isupper() != piece.isupper()):
            return False

        step = 1 if rook_y > start_y else -1
        for y in range(start_y + step, rook_y, step):
            if self.get_piece(start_x, y) != ' ':
                return False

        opponent = 'black' if color == 'white' else 'white'
        for y in [start_y, start_y + step, dest_y]:
            if self.check_if_in_check(start_x, y, opponent):
                return False

        return True

    def update_game_status(self):
        """Update game_status based on current board state."""
        color = self.turn
        in_check = self.is_in_check(color)
        has_moves = self.has_legal_moves(color)

        if in_check and not has_moves:
            self.game_status = 'checkmate'
        elif not in_check and not has_moves:
            self.game_status = 'stalemate'
        elif in_check:
            self.game_status = 'check'
        else:
            self.game_status = 'active'

    def update_state(self, new_state):
        self.board = new_state.board
        self.move_history = new_state.move_history
        self.turn = new_state.turn
        self.score = new_state.score

def main():
    chess_board = ChessBoard()

if __name__ == "__main__":
    main()