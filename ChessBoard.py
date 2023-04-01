class ChessBoard:
    def __init__(self):
        self.piece_values = {'p': 1, 'r': 5, 'n': 3, 'b': 3, 'q': 9, 'k': 0}
        self.score = {'white': 0, 'black': 0}
        self.turn = 'white'

        self.move_history = []
        self.board = [[' ' for _ in range(8)] for _ in range(8)]
        self.initialize_board()

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

        if destination_piece != ' ' and piece.islower() == destination_piece.islower():
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

        if is_valid_move:
            prev_piece = self.get_piece(dest_x, dest_y)
            score_change = 0
            prev_piece_value = 0
            if prev_piece != ' ':
                prev_piece_value = self.piece_values[prev_piece.lower()]
                if prev_piece.isupper():
                    self.score['black'] += prev_piece_value
                else:
                    self.score['white'] += prev_piece_value

            self.set_piece(dest_x, dest_y, piece)
            self.set_piece(start_x, start_y, ' ')

            self.move_history.append(((start_x, start_y), (dest_x, dest_y), prev_piece, score_change))
            print("Current list of move history: " + str(self.move_history))
            print("Current score: " + str(self.get_score()))
            self.turn = 'black' if self.turn == 'white' else 'white'
            return True
        return False

    def get_score(self):
        return self.score

    def undo_move(self):
        if not self.move_history:
            return False

        last_move = self.move_history.pop()
        (start_x, start_y), (dest_x, dest_y), prev_piece, score_change = last_move

        moved_piece = self.get_piece(dest_x, dest_y)
        self.board[start_x][start_y] = moved_piece

        self.board[dest_x][dest_y] = prev_piece

        if prev_piece != ' ':
            if prev_piece.isupper():
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

    def valid_pawn_move(self, start_x, start_y, dest_x, dest_y):
        piece = self.get_piece(start_x, start_y)
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

def main():
    chess_board = ChessBoard()

    chess_board.move_piece(1, 4, 3, 4)
    chess_board.move_piece(6, 3, 4, 3)

    chess_board.print_board()

if __name__ == "__main__":
    main()