import pygame
from ChessBoard import ChessBoard
from GUI import draw_board, draw_help_menu, draw_import_export_menu, draw_menu, draw_transparent_background, draw_scoreboard, load_images, SQUARE_SIZE, WIDTH, HEIGHT, import_export_function
from Network import Network
from pygame_textinput.pygame_textinput import TextInputManager, TextInputVisualizer
import os
import ipaddress
import sys

def decode_import(valid_import):
    import re

    # Function to convert algebraic notation to row and column
    def algebraic_to_coord(move):
        col_map = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
        return 8 - int(move[1]), col_map[move[0]]

    # Regular expression pattern for a standard chess move
    move_pattern = re.compile(
        r"^(?P<piece>[KQRBN]?)(?P<col>[a-h]?)(?P<row>[1-8]?)(?P<capture>x?)(?P<dest_col>[a-h])(?P<dest_row>[1-8])(?P<promotion>=[QRBN])?(?P<check>[+#]?)$"
    )

    # Split the valid_import into individual moves
    moves = valid_import.split(', ')

    decoded_moves = []

    for move in moves:
        match = move_pattern.match(move)
        if match:
            piece = match.group('piece')
            start_col = match.group('col')
            start_row = match.group('row')
            dest_col = match.group('dest_col')
            dest_row = match.group('dest_row')

            # If the start_col and start_row are not specified, set them to the destination coordinates
            start_coord = (algebraic_to_coord(start_col + start_row) if start_row and start_col else algebraic_to_coord(dest_col + dest_row))
            dest_coord = algebraic_to_coord(dest_col + dest_row)

            decoded_moves.append((piece, start_coord, dest_coord))

    return decoded_moves

def is_valid_import(import_string):
    if import_string == "":
        print("DEBUG: String empty!")
        return False
    import re
    # Regular expression pattern for a standard chess move
    move_pattern = re.compile(
        r"^(?P<piece>[KQRBN]?)(?P<col>[a-h]?)(?P<row>[1-8]?)(?P<capture>x?)(?P<dest_col>[a-h])(?P<dest_row>[1-8])(?P<promotion>=[QRBN])?(?P<check>[+#]?)$"
    )

    # Split the import_string into individual moves
    moves = import_string.split(", ")
    # Check if each move in the import_string is valid
    for move in moves:
        if not move_pattern.match(move):
            print("DEBUG: String not empty, but malformed! (" + str(import_string) + ")")
            return False

    return True

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess")
    load_images()

    def show_alert_message(message, width, height):
        # Create a surface for the alert
        alert_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        alert_surface.fill((50, 50, 50, 180))  # Semi-transparent background

        # Render the message text
        font = pygame.font.Font(None, 24)
        lines = message.split('\n')
        for i, line in enumerate(lines):
            text = font.render(line, True, (255, 255, 255))  # White text
            text_rect = text.get_rect(center=(width // 2, (i * 30) + (height // 2) - 30))
            alert_surface.blit(text, text_rect)

        # Draw the alert surface on the screen
        screen.blit(alert_surface, ((screen.get_width() - width) // 2, (screen.get_height() - height) // 2))
        pygame.display.flip()

        # Wait for ESC key to exit
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return


    network = Network()
    chess_board = ChessBoard()
    file_path_import = "import.txt"
    if os.path.exists(file_path_import):
        with open(file_path_import, "r") as f:
            contents = f.read()
            if contents == "":
                contents = "Empty!"
            print("Import file detected! Contents: " + contents)


    game_state = "menu"  # Add a state variable for the game
    menu_buttons = []
    
    text_input_manager_help = TextInputManager()  # Initialize TextInputManager
    text_input_visualizer_help = TextInputVisualizer(manager=text_input_manager_help)
    text_input_manager_import = TextInputManager()
    text_input_visualizer_import = TextInputVisualizer(manager=text_input_manager_import)

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
                        game_state = "import"
                    elif button["function"] == "back":
                        game_state = "menu"
                    elif button["function"] == "quit_game":  # Add this condition
                        pygame.quit()
                        sys.exit()
            return game_state

    def draw_scoreboard_background(screen):
        BACKGROUND_WIDTH, BACKGROUND_HEIGHT = 400, 200
        BACKGROUND_COLOR = (153, 102, 51)
        BACKGROUND_BORDER_COLOR = (0, 0, 0)
        background_rect = pygame.Rect((WIDTH - BACKGROUND_WIDTH) // 2, (HEIGHT - BACKGROUND_HEIGHT) // 2, BACKGROUND_WIDTH, BACKGROUND_HEIGHT)
        pygame.draw.rect(screen, BACKGROUND_COLOR, background_rect)
        pygame.draw.rect(screen, BACKGROUND_BORDER_COLOR, background_rect, 5)

    def is_valid_ip(ip_string):
        try:
            if (ip_string == ""):
                return False
            ipaddress.ip_address(ip_string)
            return True
        except ValueError:
            return False

    def draw_menu_background(screen):
        BACKGROUND_WIDTH, BACKGROUND_HEIGHT = 700, 500  # Increase width to 700 and height to 500
        BACKGROUND_COLOR = (153, 102, 51)
        BACKGROUND_BORDER_COLOR = (0, 0, 0)
        background_rect = pygame.Rect((WIDTH - BACKGROUND_WIDTH) // 2, (HEIGHT - BACKGROUND_HEIGHT) // 2, BACKGROUND_WIDTH, BACKGROUND_HEIGHT)
        pygame.draw.rect(screen, BACKGROUND_COLOR, background_rect)
        pygame.draw.rect(screen, BACKGROUND_BORDER_COLOR, background_rect, 5)

    running = True
    selected_piece = None
    textbox_rect = None
    mouse_button_released = True  # Add this line before the loop
    shown = False
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and mouse_button_released:
                mouse_button_released = False
                x, y = pygame.mouse.get_pos()
                if game_state in ["menu", "help", "import"]:
                    x, y = pygame.mouse.get_pos()
                    game_state = handle_menu_click((x, y), game_state, menu_buttons, textbox_rect)
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_button_released = True

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:  # Fix the indentation here
                if event.key == pygame.K_u and game_state == "play":
                    chess_board.undo_move(False)
                elif event.key == pygame.K_ESCAPE and game_state == "play":
                    game_state = "menu"
                elif event.key == pygame.K_ESCAPE and game_state == "scoreboard":
                    game_state = "menu"
                elif event.key == pygame.K_ESCAPE and game_state == "help":
                    game_state = "menu"
                elif event.key == pygame.K_ESCAPE and game_state == "menu":
                    game_state = "play"
                elif event.key == pygame.K_ESCAPE and game_state == "import":
                    game_state = "menu"
                elif event.key == pygame.K_DELETE and game_state == "import":
                    file_path = "import.txt"
                    if os.path.exists(file_path):
                        show_alert_message("IMPORT FILE CLEARED! \n(press ESC to exit)", 300, 100)
                        with open(file_path, "w") as f:
                            f.write("")
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
            file_path = "server.txt"
            if not os.path.exists(file_path) and not shown:
                shown = True
                show_alert_message("IP FILE MISSING! \nPLEASE CREATE server.txt! \n(press ESC to exit)", 300, 100)
            elif os.path.exists(file_path) and not shown:
                with open(file_path, "r") as f:
                    if f.read() == "":
                        shown = True
                        show_alert_message("IP FILE EMPTY! \n EDIT IN HELP MENU! \n(press ESC to exit)", 300, 100)
        elif game_state == "help":
            draw_transparent_background(screen)
            draw_menu_background(screen)
            menu_buttons, textbox_rect = draw_help_menu(screen, text_input_visualizer_help, events)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                input_text_help = text_input_manager_help.value  # Get the input from the text_input_manager
                print("DEBUG: input_text_help value: " + str(input_text_help))
                file_path_one = "server.txt"

                if not os.path.exists(file_path_one):
                    with open(file_path_one, "w") as f:
                        pass  # You can write some initial content here if you want, or just leave it empty
                with open("server.txt", "r") as f:
                    if not is_valid_ip(f.read()):
                        print("Invalid or empty IP!")
                        with open("server.txt", "w") as f:
                            f.write(input_text_help)  # Update the server.txt file with the input
                # Update the server_data variable in Network.py
                Network.server_data = input_text_help
                #print(input_text)
                text_input_manager_help.clear_text()  # Clear the input after updating the file
        elif game_state == "import":
            draw_transparent_background(screen)
            draw_menu_background(screen)
            menu_buttons, textbox_rect = draw_import_export_menu(screen, text_input_visualizer_import, events)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                input_text_import = text_input_manager_import.value  # Get the input from the text_input_manager
                file_path_two = "import.txt"

                if not os.path.exists(file_path_two):
                    with open(file_path_two, "w") as f:
                        pass  # You can write some initial content here if you want, or just leave it empty
                with open("import.txt", "r") as f:
                    if f.read() == "" or input_text_import != "":
                        with open("import.txt", "w") as f:
                            f.write(input_text_import)  # Update the server.txt file with the input
                print("DEBUG: Is valid input?: " + str(is_valid_import(input_text_import)))
                if input_text_import != "" and is_valid_import(input_text_import):
                    decoded_moves = decode_import(input_text_import)
                    for move in decoded_moves:
                        piece, start_coord, dest_coord = move
                        start_x, start_y = start_coord
                        dest_x, dest_y = dest_coord
                        chess_board.move_piece(start_x, start_y, dest_x, dest_y)
                
                # Update the server_data variable in Network.py
                Network.server_data = input_text_import
                #print(input_text)
                text_input_manager_import.clear_text() #ar the input after updating the filee file

        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    main()