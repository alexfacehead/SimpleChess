import pygame
from ChessBoard import ChessBoard
from GUI import draw_board, draw_help_menu, draw_menu, draw_transparent_background, draw_scoreboard, load_images, SQUARE_SIZE, WIDTH, HEIGHT, import_export_function
from Network import Network
from pygame_textinput.pygame_textinput import TextInputManager


def main():
    network = Network()
    chess_board = ChessBoard()

    game_state = "menu"  # Add a state variable for the game
    menu_buttons = []

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess")
    load_images()
    
    text_input_manager = TextInputManager()  # Initialize TextInputManager

    def handle_menu_click(pos, game_state, menu_buttons, textbox_rect=None):
        if (WIDTH // 2 - 300) // 2 <= pos[0] <= (WIDTH * 3 // 2 + 300) // 2 and (HEIGHT // 2 - 200) // 2 <= pos[1] <= (HEIGHT * 3 // 2 + 200) // 2:
            for button in menu_buttons:
                if button["rect"].collidepoint(pos):
                    if button["function"] == "resume":
                        game_state = "play"
                    elif button["function"] == "scoreboard":
                        game_state = "scoreboard"
                    elif button["function"] == "help":
                        game_state = "help"
                    elif button["function"] == "import_export":
                        import_export_function()
                    elif button["function"] == "back":
                        game_state = "menu"
        return game_state

    def draw_scoreboard_background(screen):
        BACKGROUND_WIDTH, BACKGROUND_HEIGHT = 400, 200
        BACKGROUND_COLOR = (153, 102, 51)
        BACKGROUND_BORDER_COLOR = (0, 0, 0)
        background_rect = pygame.Rect((WIDTH - BACKGROUND_WIDTH) // 2, (HEIGHT - BACKGROUND_HEIGHT) // 2, BACKGROUND_WIDTH, BACKGROUND_HEIGHT)
        pygame.draw.rect(screen, BACKGROUND_COLOR, background_rect)
        pygame.draw.rect(screen, BACKGROUND_BORDER_COLOR, background_rect, 5)

    def draw_menu_background(screen):
        BACKGROUND_WIDTH, BACKGROUND_HEIGHT = 600, 400
        BACKGROUND_COLOR = (153, 102, 51)
        BACKGROUND_BORDER_COLOR = (0, 0, 0)
        background_rect = pygame.Rect((WIDTH - BACKGROUND_WIDTH) // 2, (HEIGHT - BACKGROUND_HEIGHT) // 2, BACKGROUND_WIDTH, BACKGROUND_HEIGHT)
        pygame.draw.rect(screen, BACKGROUND_COLOR, background_rect)
        pygame.draw.rect(screen, BACKGROUND_BORDER_COLOR, background_rect, 5)

    running = True
    selected_piece = None
    textbox_rect = None
    mouse_button_released = True  # Add this line before the loop
    textbox_clicked = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and mouse_button_released:  # Add the condition here
                mouse_button_released = False
                x, y = pygame.mouse.get_pos()
                game_state = handle_menu_click((x, y), game_state, menu_buttons, textbox_rect)
            elif event.type == pygame.MOUSEBUTTONUP:  # Add this condition
                mouse_button_released = True
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
                                updated_board = network.send((selected_piece[0], selected_piece[1], row, col))
                                if updated_board is not None:  # Add this check
                                    chess_board = updated_board
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
        if game_state == "help":
            draw_transparent_background(screen)
            draw_menu_background(screen)
            menu_buttons, textbox_rect = draw_help_menu(screen, text_input_manager)

            # Input handling logic for the textbox goes here
            if textbox_clicked and mouse_button_released:
                input_text = text_input_manager.get_text() # Get the input from the text_input_manager # Get the input from the text_input_manager
                with open("server.txt", "w") as f:
                    f.write(input_text)  # Update the server.txt file with the input
                print(input_text)
                text_input_manager.clear_input()  # Clear the input after updating the file
                textbox_clicked = False
            elif textbox_rect and textbox_rect.collidepoint(pygame.mouse.get_pos()):
                textbox_clicked = True

        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    main()