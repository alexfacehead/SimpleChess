import pygame
from ChessBoard import ChessBoard
from GUI import draw_board, draw_menu, SQUARE_SIZE, WIDTH, HEIGHT

def main():
    global chess_board
    chess_board = ChessBoard()
    DEBUG_FLAG = True
    RED = (255, 0, 0)

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess")

    def draw_score(screen, chess_board):
        font = pygame.font.Font(None, 48)
        score = chess_board.get_score()
        white_score_text = font.render(f"White: {score['white']}", True, RED)
        black_score_text = font.render(f"Black: {score['black']}", True, RED)

        screen.blit(white_score_text, (10, 10))

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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_u:
                    chess_board.undo_move()

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                col, row = x // SQUARE_SIZE, y // SQUARE_SIZE
                piece = chess_board.get_piece(row, col)

                if not selected_piece and piece != ' ':
                    selected_piece = (row, col)
                    king_selected = piece.lower() == 'k'
                elif selected_piece:
                    if row == selected_piece[0] and col == selected_piece[1]:
                        selected_piece = None
                        king_selected = False
                    else:
                        if DEBUG_FLAG:
                            chess_board.print_board()
                            print(f"start_x: {selected_piece[0]}, start_y: {selected_piece[1]}, dest_x: {row}, dest_y: {col}")

                        move_successful = chess_board.move_piece(selected_piece[0], selected_piece[1], row, col)

                        if move_successful:
                            selected_piece = None
                            king_selected = False
                        elif piece != ' ':
                            selected_piece = (row, col)
                            king_selected = piece.lower() == 'k'

        draw_board(screen, chess_board, selected_piece)
        draw_menu(screen)  # Add this line
        draw_score(screen, chess_board)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()