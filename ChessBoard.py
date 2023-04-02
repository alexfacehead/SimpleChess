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

    # For formatting
    def get_pos(x, y):
        pos_map = {
            0: 'a',
            1: 'b',
            2: 'c',
            3: 'd',
            4: 'e',
            5: 'f',
            6: 'g',
            7: 'h'
        }
        return pos_map[y] + str(8 - x)  # Swap x and y, and subtract x from 8

    def initialize_board(self):
        pieces = ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']

        for i, piece in enumerate(pieces):
            self.board[0][i] = piece
            self.board[7][i] = piece.lower()

        for i in range(8):
            self.board[1][i] = 'P'
            self.board[6][i] = 'p'

    def get_piece(self, x, y):
        return self.board[x][y]

    def set_piece(self, x, y, piece):
        self.board[x][y] = piece

    def move_piece(self, start_x, start_y, dest_x, dest_y):
        piece = self.get_piece(start_x, start_y)
        destination_piece = self.get_piece(dest_x, dest_y)
        if (piece.isupper() and self.turn == 'black') or (piece.islower() and self.turn == 'white'):
            return False

        is_castle_move = piece.lower() == "k" and abs(dest_y - start_y) > 1
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

        if piece_type in valid_move_methods:
            is_valid_move = valid_move_methods[piece_type](start_x, start_y, dest_x, dest_y)
            if (is_castle_move):
                is_valid_move = True

        if is_valid_move:
            if is_castle_move:
                if not self.handle_castling_conditions(start_x, start_y, dest_x, dest_y):
                    return False
                self.move_history.append(((start_x, start_y), (dest_x, dest_y), piece, 0))
                self.turn = 'black' if self.turn == 'white' else 'white'
            else:
                score_gain = 0
                if destination_piece != ' ':
                    print("DEBUG: Setting score_gain")
                    score_gain = self.piece_values[destination_piece.lower()]
                    print("DEBUG: Score_gain = " + str(score_gain))
                    if destination_piece.islower():
                        print("Adding to white score")
                        self.score['white'] += score_gain
                    else:
                        self.score['black'] += score_gain
                self.set_piece(dest_x, dest_y, piece)
                self.set_piece(start_x, start_y, ' ')
                self.move_history.append(((start_x, start_y), (dest_x, dest_y), piece, score_gain))
                print("DEBUG: Move history: " + str(self.move_history))
                if piece_type == "r" and start_x == 0:
                    if start_y == 0:
                        self.queen_rook_moved[self.turn] = True
                    elif start_y == 7:
                        self.king_rook_moved[self.turn] = True
                elif piece_type == "r" and start_x == 7:
                    if start_y == 0:
                        self.queen_rook_moved[self.turn] = True
                    elif start_y == 7:
                        self.king_rook_moved[self.turn] = True
                self.turn = 'black' if self.turn == 'white' else 'white'
                return True
        return False

    def handle_castling_conditions(self, start_x, start_y, dest_x, dest_y):
        print("DEBUG: Handling castling block entered")
        piece = self.get_piece(start_x, start_y)
        color = 'white' if piece.isupper() else 'black'

        if self.king_moved[color] or ((dest_y == 0 and self.queen_rook_moved[color]) or (dest_y == 7 and self.king_rook_moved[color])):
            print("DEBUG: Returning false from handling castling. self.king_moved[" + str(color) + "]" + "=" + str(self.king_moved[color]))
            print("DEBUG: self.king_moved[" + str(color) + "]" + "=" + str(self.queen_rook_moved[color]))
            print("DEBUG: dest_y == 7 = " + str(dest_y == 7) + " and self.king_rook_moved[" + str(color) + "]" + "=" + str(self.king_rook_moved[color]))
            return False

        is_short_castling = dest_y == start_y + 3
        is_long_castling = dest_y == start_y - 4

        if not (is_short_castling or is_long_castling):
            print("DEBUG: Returning false from handling castling because not is_short_castling and not is_long_castling")
            return False

        if is_short_castling:
            if not self.is_clear_for_castle(start_y, start_y, dest_x, dest_y):
                print("DEBUG: Returning false from handling castling because path is not clear #1")
                return False
        else:
            if not self.is_clear_for_castle(start_y, start_y, dest_x, dest_y):
                print("DEBUG: Returning false from handling castling because path is not clear #2")
                return False

        if not self.check_if_in_check(start_x, start_y, self.turn):
            print("DEBUG: Entering final handle_castling block, not in check")
            print("DEBUG: Rook y: " + str(dest_y))
            print("DEBUG: King y: " + str(start_y))
            self.perform_castle(start_x, start_y, dest_x, dest_y, is_short_castling)
            self.move_history.append(((start_x, start_y), (dest_x, dest_y), piece, 0))
            print("DEBUG: Castling performed: {} to {}".format(ChessBoard.get_pos(start_x, start_y), ChessBoard.get_pos(dest_x, dest_y)))
            print("Current list of move history: " + str(self.move_history))
            print("Current score: " + str(self.get_score()))
            #self.turn = 'black' if self.turn == 'white' else 'white'
            return True
        return False
    
    def is_space_empty(self, x, y):
        return self.get_piece(x, y) == ' '

    def is_clear_for_castle(self, start_x, start_y, dest_x, dest_y):
        print("DEBUG: Checking if path is clear for castle")
        step = 1 if start_y < dest_y else -1
        for y in range(start_y + step, dest_y, step):
            if not self.is_space_empty(dest_x, y):
                return False
        print("DEBUG: Path is clear!")
        return True

    def check_if_in_check(self, king_x, king_y, turn):
        for x in range(8):
            for y in range(8):
                piece = self.get_piece(x, y)
                if piece != ' ' and (piece.isupper() != (turn == 'white')):
                    piece_type = piece.lower()
                    valid_move_methods = {
                        'r': self.valid_rook_move,
                        'n': self.valid_knight_move,
                        'b': self.valid_bishop_move,
                        'q': self.valid_queen_move,
                        'k': self.valid_king_move,
                        'p': self.valid_pawn_move
                    }

                    if piece_type in valid_move_methods:
                        is_valid_move = valid_move_methods[piece_type](x, y, king_x, king_y)
                        if is_valid_move:
                            return True
        return False

    def perform_castle(self, king_x, king_y, rook_x, rook_y, is_short_castling):
        print("Performing the castling (set_piece attempt is to follow)")
        king_destination_y = king_y + 2 if is_short_castling else king_y - 2
        self.set_piece(king_x, king_destination_y, self.get_piece(king_x, king_y))
        self.set_piece(king_x, king_y, ' ')

        rook_destination_y = king_destination_y - 1 if is_short_castling else king_destination_y + 1
        self.set_piece(king_x, rook_destination_y, self.get_piece(rook_x, rook_y))
        self.set_piece(rook_x, rook_y, ' ')

        if self.get_piece(king_x, king_destination_y).isupper():
            self.king_moved['white'] = True
            if rook_y < king_y:
                self.queen_rook_moved['white'] = True
            else:
                self.king_rook_moved['white'] = True
        elif self.get_piece(king_x, king_destination_y).islower():
            print("Setting king_moved['black'] to True #1")
            self.king_moved['black'] = True
            if rook_y < king_y:
                self.queen_rook_moved['black'] = True
            else:
                print("Setting king_moved['black'] to True #2")
                self.king_rook_moved['black'] = True
        print("End of perform castle")

    def get_score(self):
        return self.score

    # New undo move undos every move including castling + scores
    def undo_move(self):
        print("Attempting undo")
        if not self.move_history:
            print("Not move history")
            return False

        last_move = self.move_history.pop()
        (start_x, start_y), (dest_x, dest_y), moved_piece, score_change = last_move

        is_castle_move = moved_piece.lower() == "k" and abs(dest_y - start_y) > 1

        if is_castle_move:
            # Determine if it was a short or long castling
            is_short_castling = dest_y > start_y

            # Undo king move
            self.set_piece(start_x, start_y, moved_piece)
            self.set_piece(dest_x, dest_y, ' ')

            # Undo rook move
            if is_short_castling:
                self.set_piece(start_x, start_y + 1, 'R' if moved_piece == 'K' else 'r')
                self.set_piece(start_x, dest_y - 1, ' ')
            else:
                self.set_piece(start_x, start_y - 1, 'R' if moved_piece == 'K' else 'r')
                self.set_piece(start_x, dest_y + 1, ' ')
                self.set_piece(start_x, dest_y + 2, ' ')  # Fix the issue with the leftover rook

            # Reset king_rook_moved, queen_rook_moved, and king_moved
            color = 'white' if moved_piece.isupper() else 'black'
            if is_short_castling:
                self.king_rook_moved[color] = False
                self.set_piece(start_x, 7, 'R' if moved_piece == 'K' else 'r')  # Move the rook back to its original position
                self.set_piece(start_x, 5, ' ')  # Remove the rook from its moved position
            else:
                self.queen_rook_moved[color] = False
                self.set_piece(start_x, 0, 'R' if moved_piece == 'K' else 'r')  # Move the rook back to its original position
                self.set_piece(start_x, 3, ' ')  # Remove the rook from its moved position
            self.king_moved[color] = False

        else:
            self.set_piece(start_x, start_y, moved_piece)
            self.set_piece(dest_x, dest_y, ' ')

            if score_change != 0:
                if moved_piece.isupper():
                    self.score['white'] -= score_change
                else:
                    self.score['black'] -= score_change

        self.turn = 'black' if self.turn == 'white' else 'white'

        return True

    # Press `u` to undo any move!
    def undo_move_old(self):
        print("Attempting undo")
        if not self.move_history:
            print("Not move history")
            return False

        last_move = self.move_history.pop()
        (start_x, start_y), (dest_x, dest_y), moved_piece, score_change = last_move
        
        is_castle_move = moved_piece.lower() == "k" and abs(dest_y - start_y) > 1

        if is_castle_move:
            # Undo king move
            self.board[start_x][start_y] = moved_piece
            self.board[dest_x][dest_y] = ' '
            
            # Determine if it was a short or long castling
            is_short_castling = dest_y > start_y

            # Undo rook move
            if is_short_castling:
                self.board[start_x][start_y + 1] = 'R' if moved_piece == 'K' else 'r'
                self.board[start_x][dest_y - 1] = ' '
            else:
                # Remove duplicate king from C1
                self.board[start_x][dest_y + 1] = ' '
                # Set the rook back to where it was
                self.board[start_x][start_y - 1] = 'R' if moved_piece == 'K' else 'r'
                self.board[start_x][dest_y - 2] = ' '

        else:
            self.board[start_x][start_y] = moved_piece
            self.board[dest_x][dest_y] = ' '

            if score_change != 0:
                if moved_piece.isupper():
                    self.score['white'] -= score_change
                else:
                    self.score['black'] -= score_change

        self.turn = 'black' if self.turn == 'white' else 'white'

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

    def do_pawn_promotion(self, dest_x, dest_y, isupper):
        print("Attempting pawn promotion")
        temp_piece = 'q'
        val = -1
        if isupper:
            temp_piece = 'Q'
            val = 1
        self.set_piece(dest_x, dest_y, temp_piece)
        self.set_piece(dest_x - val, dest_y, ' ')
        print("Finished pawn promotion")
        return True
    
    def valid_pawn_move(self, start_x, start_y, dest_x, dest_y):
        piece = self.get_piece(start_x, start_y)
        print ("DEBUG: piece.islower == " + str(piece.islower()))
        if (piece.isupper() and dest_x == 7 or piece.islower() and dest_x == 0) and piece.lower() == 'p':
            print("Pawn promotion square reached")
            #self.do_pawn_promotion(dest_x, dest_y, piece.isupper())
        is_white = piece.isupper()
        direction = 1 if is_white else -1
        dest_piece = self.get_piece(dest_x, dest_y)

        if dest_y == start_y and dest_x == start_x + direction and dest_piece == ' ':
            return True

        if abs(dest_y - start_y) == 1 and dest_x == start_x + direction and dest_piece != ' ' and dest_piece.isupper() != is_white:
            destination_piece_present = self.get_piece(dest_x, dest_y) != ' '
            if destination_piece_present:
                return True

        if (start_x == 1 and is_white) or (start_x == 6 and not is_white):
            if dest_y == start_y and dest_x == start_x + 2 * direction and dest_piece == ' ' and self.get_piece(start_x + direction, start_y) == ' ':
                return True

        return False

    def valid_king_move(self, start_x, start_y, dest_x, dest_y):
        x_diff = abs(start_x - dest_x)
        y_diff = abs(start_y - dest_y)

        if x_diff <= 1 and y_diff <= 1:
            return True
        else:
            return False

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

def main():
    chess_board = ChessBoard()

if __name__ == "__main__":
    main()