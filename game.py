import pygame
from ChessBoard import ChessBoard
from GUI import draw_board, draw_menu, SQUARE_SIZE, WIDTH, HEIGHT

def main():
    global chess_board
    chess_board = ChessBoard()
    DEBUG_FLAG = True
    RED = (0, 0, 0)

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess")

    def draw_text_with_border(text, font, color, bgcolor, x, y, screen):
        text_surf = font.render(text, True, color)

        bg_surf = font.render(text, True, bgcolor)
        for i in range(-2, 3):
            for j in range(-2, 3):
                if i != 0 or j != 0:
                    screen.blit(bg_surf, (x + i, y + j))

        screen.blit(text_surf, (x, y))

    def draw_score(screen, chess_board):
        font = pygame.font.Font(None, 48)
        score = chess_board.get_score()
        white_score_text = f"White: {score['white']}"
        black_score_text = f"Black: {score['black']}"

        draw_text_with_border(white_score_text, font, RED, (255, 255, 255), 10, 10, screen)

        black_score_width = font.size(black_score_text)[0]
        black_score_height = font.size(black_score_text)[1]
        margin = 10
        black_score_x = WIDTH - black_score_width - margin
        black_score_y = HEIGHT - black_score_height - margin

        draw_text_with_border(black_score_text, font, RED, (255, 255, 255), black_score_x, black_score_y, screen)

    running = True
    selected_piece = None
    king_selected = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_u:
                    chess_board.undo_move(False)

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
        draw_menu(screen)
        draw_score(screen, chess_board)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()