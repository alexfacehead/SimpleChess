import pygame
from ChessBoard import ChessBoard
from GUI import draw_board, draw_menu, draw_transparent_background, draw_scoreboard, load_images, SQUARE_SIZE, WIDTH, HEIGHT, help_function, import_export_function
from network import Network

def main():
    chess_board = ChessBoard()

    game_state = "menu"  # Add a state variable for the game
    menu_buttons = []

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess")
    load_images()

    def handle_menu_click(pos):
        nonlocal game_state
        if (WIDTH // 2 - 300) // 2 <= pos[0] <= (WIDTH * 3 // 2 + 300) // 2 and (HEIGHT // 2 - 200) // 2 <= pos[1] <= (HEIGHT * 3 // 2 + 200) // 2:
            for button in menu_buttons:
                if button["rect"].collidepoint(pos):
                    if button["function"] == "resume":
                        game_state = "play"
                    elif button["function"] == "scoreboard":
                        game_state = "scoreboard"
                        draw_scoreboard(screen, chess_board)
                        #draw_score(screen, chess_board)
                        pygame.display.update()
                    elif button["function"] == "help":
                        help_function()
                    elif button["function"] == "import_export":
                        import_export_function()

    def draw_text_with_border(text, font, color, bgcolor, x, y, screen):
        text_surf = font.render(text, True, color)

        bg_surf = font.render(text, True, bgcolor)
        for i in range(-2, 3):
            for j in range(-2, 3):
                if i != 0 or j != 0:
                    screen.blit(bg_surf, (x + i, y + j))

        screen.blit(text_surf, (x, y))

    def draw_scoreboard_background(screen):
        BACKGROUND_WIDTH, BACKGROUND_HEIGHT = 400, 200
        BACKGROUND_COLOR = (153, 102, 51)
        BACKGROUND_BORDER_COLOR = (0, 0, 0)
        background_rect = pygame.Rect((WIDTH - BACKGROUND_WIDTH) // 2, (HEIGHT - BACKGROUND_HEIGHT) // 2, BACKGROUND_WIDTH, BACKGROUND_HEIGHT)
        pygame.draw.rect(screen, BACKGROUND_COLOR, background_rect)
        pygame.draw.rect(screen, BACKGROUND_BORDER_COLOR, background_rect, 5)

    def draw_score_obsolete(screen, chess_board):
        font = pygame.font.Font(None, 48)
        score = chess_board.get_score()
        white_score_text = f"White: {score['white']}"
        black_score_text = f"Black: {score['black']}"

        draw_text_with_border(white_score_text, font, (0, 0, 0), (255, 255, 255), 10, 10, screen)

        black_score_width = font.size(black_score_text)[0]
        black_score_height = font.size(black_score_text)[1]
        margin = 10
        black_score_x = WIDTH - black_score_width - margin
        black_score_y = HEIGHT - black_score_height - margin

        draw_text_with_border(black_score_text, font, (0, 0, 0), (255, 255, 255), black_score_x, black_score_y, screen)

    running = True
    selected_piece = None
    while running:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if game_state == "menu":
                    handle_menu_click((x, y))

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_u and game_state == "play":
                    chess_board.undo_move(False)
                elif event.key == pygame.K_ESCAPE:
                    game_state = "menu"

            if event.type == pygame.QUIT:
                running = False

            # Add a condition to check if game_state is "play"
            if game_state == "play":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    col, row = x // SQUARE_SIZE, y // SQUARE_SIZE
                    piece = chess_board.get_piece(row, col)

                    if not selected_piece and piece != ' ':
                        selected_piece = (row, col)
                    elif selected_piece:
                        if row == selected_piece[0] and col == selected_piece[1]:
                            selected_piece = None
                        else:
                            move_successful = chess_board.move_piece(selected_piece[0], selected_piece[1], row, col)

                            if move_successful:
                                chess_board = Network.network.send((selected_piece[0], selected_piece[1], row, col))
                                selected_piece = None
                            elif piece != ' ':
                                selected_piece = (row, col)
        draw_board(screen, chess_board, selected_piece)

        if game_state == "play":
            draw_board(screen, chess_board, selected_piece)
        elif game_state == "scoreboard":
            draw_transparent_background(screen)
            draw_scoreboard_background(screen)  # Add this line
            draw_scoreboard(screen, chess_board)
        elif game_state == "menu":
            draw_transparent_background(screen)
            menu_buttons = draw_menu(screen, "main")

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()