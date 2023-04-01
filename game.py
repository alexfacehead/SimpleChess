import pygame
from ChessBoard import ChessBoard
from GUI import draw_board, SQUARE_SIZE, WIDTH, HEIGHT

def main():
    global chess_board
    chess_board = ChessBoard()
    DEBUG_FLAG = True
    RED = (255, 0, 0)

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess")

    # Function to handle graphical score display
    # Function to handle graphical score display
    def draw_score(screen, chess_board):
        font = pygame.font.Font(None, 48)  # Increased font size to 48
        score = chess_board.get_score()
        white_score_text = font.render(f"White: {score['white']}", True, RED)
        black_score_text = font.render(f"Black: {score['black']}", True, RED)

        screen.blit(white_score_text, (10, 10))

        # Calculate the position of the black score text by taking into account the
        # width of the text and a margin from the right and bottom edges of the screen
        black_score_width = black_score_text.get_width()
        black_score_height = black_score_text.get_height()
        margin = 10
        black_score_x = WIDTH - black_score_width - margin
        black_score_y = HEIGHT - black_score_height - margin

        screen.blit(black_score_text, (black_score_x, black_score_y))

    running = True
    selected_piece = None
    king_selected = False
    while running:
        for event in pygame.event.get():
            # undo / key press event
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_u:
                    chess_board.undo_move()

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                col, row = x // SQUARE_SIZE, y // SQUARE_SIZE  # Swap col and row
                piece = chess_board.get_piece(row, col)

                if not selected_piece and piece != ' ':
                    selected_piece = (row, col)
                    king_selected = piece.lower() == 'k'  # Check if the king is selected
                elif selected_piece:
                    if row == selected_piece[0] and col == selected_piece[1]:  # Deselect the selected piece if clicked again
                        selected_piece = None
                        king_selected = False
                    else:
                        # DEBUG BLOCK, ALTER DEBUG_FLAG TO BE FALSE IF YOU DON'T WANT BOARD STATE PRINTED TO CONSOLE
                        if DEBUG_FLAG:
                            chess_board.print_board()
                            print(f"start_x: {selected_piece[0]}, start_y: {selected_piece[1]}, dest_x: {row}, dest_y: {col}")
                        
                        if king_selected and piece.lower() == 'r' and piece.islower() == chess_board.get_piece(selected_piece[0], selected_piece[1]).islower() and abs(col - selected_piece[1]) == 3:
                            move_successful = chess_board.move_piece(selected_piece[0], selected_piece[1], row, col)
                        else:
                            move_successful = chess_board.move_piece(selected_piece[0], selected_piece[1], row, col)  # No need to swap row and col

                        if move_successful:
                            selected_piece = None
                            king_selected = False
                        elif piece != ' ':  # Select a new piece if a different piece is clicked
                            selected_piece = (row, col)
                            king_selected = piece.lower() == 'k'

        # Refresh board
        draw_board(screen, chess_board)
        draw_score(screen, chess_board)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()