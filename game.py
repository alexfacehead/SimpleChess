import pygame
from ChessBoard import ChessBoard
from GUI import draw_board, draw_help_menu, draw_import_export_menu, draw_menu, draw_transparent_background, draw_scoreboard, load_images, SQUARE_SIZE, WIDTH, HEIGHT
from Network import Network
from pygame_textinput.pygame_textinput import TextInputManager, TextInputVisualizer
import os
import ipaddress
import sys
import pyperclip
import re

# Exports the current game move history to a usable format
def export_move_history(move_history):
    formatted_moves = []

    for move in move_history:
        start_x, start_y = move[0]
        dest_x, dest_y = move[1]
        formatted_moves.append((start_y, start_x, dest_y, dest_x))
    print("Exporting move list: " + str(convert_to_algebraic_notation(formatted_moves)))
    return formatted_moves

def convert_to_algebraic_notation(moves):
    converted_move_string = ""
    for move in moves:
        start = chr(ord('a') + move[1]) + str(8 - move[0])
        end = chr(ord('a') + move[3]) + str(8 - move[2])
        converted_move_string = converted_move_string + start + ", " + end
        converted_move_string = converted_move_string + ", "
    move_string_index = len(converted_move_string) - 1
    if move_string_index > 0:
        return converted_move_string[0:move_string_index-1]
    else:
        return "Empty!"

def save_moves_to_file(formatted_moves):
    file_path_three = "import.txt"
    if os.path.exists(file_path_three):
        with open(file_path_three, "w") as f:
            moves_string = convert_to_algebraic_notation(formatted_moves)
            if is_valid_import(moves_string):
                f.write(moves_string)

def is_valid_import(import_string):
    if import_string == "":
        print("DEBUG: Import string empty!")
        return False

    # Regular expression patterns for both formats
    move_pattern_old = re.compile(
        r"^(?P<piece>[KQRBN]?)(?P<col>[a-hA-H]?)(?P<row>[1-8]?)(?P<capture>x?)(?P<dest_col>[a-hA-H])(?P<dest_row>[1-8])(?P<promotion>=[QRBN])?(?P<check>[+#]?)$"
    )
    move_pattern_new = re.compile(
        r"^(?P<start_y>[0-7])\s(?P<start_x>[0-7])\s(?P<dest_y>[0-7])\s(?P<dest_x>[0-7])$"
    )

    # Strip the trailing newline character
    print("Import string: " + str(import_string))
    import_string = import_string.strip()

    # Improved delimiter detection
    comma_count = import_string.count(',')
    space_count = import_string.count(' ')

    if comma_count > space_count:
        delimiter = ','
    else:
        delimiter = ' '

    moves = re.split(r'[,\s]+', import_string)  # Update this line to split using both comma and space

    # Check if each move in the import_string is valid
    for move in moves:
        if not move_pattern_old.match(move) and not move_pattern_new.match(move):
            if import_string != "Empty!":
                print("DEBUG: String not empty, but malformed! (" + str(import_string) + ")")
            return False

    return True

    # Check if each move in the import_string is valid
    for move in moves:
        if not move_pattern_old.match(move) and not move_pattern_new.match(move):
            if import_string != "Empty!":
                print("DEBUG: String not empty, but malformed! (" + str(import_string) + ")")
            return False

    return True

    # Check if each move in the import_string is valid
    for move in moves:
        if not move_pattern_old.match(move) and not move_pattern_new.match(move):
            if import_string != "Empty!":
                print("DEBUG: String not empty, but malformed! (" + str(import_string) + ")")
            return False

    return True


def decode_import(valid_import):
    def convert_coordinate(coordinate):
        col = ord(coordinate[0].lower()) - ord('a')
        row = 8 - int(coordinate[1])  # Reverse the row index calculation
        return row, col

    valid_import = valid_import.replace(',', ' ').strip()  # Replace commas with spaces
    moves = [move.strip() for move in valid_import.split(" ") if move.strip()]  # Split the string based on spaces and remove empty strings

    decoded_moves = []

    for i in range(0, len(moves) - 1, 2):
        if moves[i] and moves[i + 1]:  # Check if both start and end coordinates are present
            start = convert_coordinate(moves[i])
            dest = convert_coordinate(moves[i + 1])
            decoded_moves.append((start[0], start[1], dest[0], dest[1]))

    return decoded_moves

def copy_to_clipboard(text):
    pyperclip.copy(text)

def paste_from_clipboard():
    return pyperclip.paste()

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess")
    load_images()
    file_path_two = "import.txt"

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
    if os.path.exists(file_path_two):
        with open(file_path_two, "r") as f:
            contents = f.read()
            if contents == "":
                contents = "Empty!"
            if is_valid_import(contents):
                decoded_moves = decode_import(contents)
                for move in decoded_moves:
                    chess_board.move_piece(*move)
    else:
        print("import.txt does not exist!")
        with open(file_path_two, "w") as f:
            print("DEBUG: import.txt does not exist. Creating now.")
            f.write("")

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
                    elif button["function"] == "export":  # Add this condition
                        formatted_moves = export_move_history(chess_board.move_history)
                        save_moves_to_file(formatted_moves)
            return game_state

    def draw_scoreboard_background(screen, BACKGROUND_WIDTH, BACKGROUND_HEIGHT):
        BACKGROUND_WIDTH, BACKGROUND_HEIGHT = BACKGROUND_WIDTH, BACKGROUND_HEIGHT
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
        
    running = True
    selected_piece = None
    textbox_rect = None
    mouse_button_released = True
    shown = False
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and mouse_button_released\
                and event.button != 2 and event.button != 3 and event.button != 4\
                    and event.button != 5:
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
                        contents = ""
                        with open(file_path, "r") as g:
                            contents  = g.read()
                        if contents != "":
                            with open(file_path, "w") as f:
                                f.write("")
                                undo_valid = chess_board.undo_move(False)
                                while chess_board is not None and undo_valid:
                                    undo_valid = chess_board.undo_move(False)
            if event.type == pygame.QUIT:
                running = False

            # Add a condition to check if game_state is "play"
            if game_state == "play":
                if event.type == pygame.MOUSEBUTTONDOWN and event.button != 2\
                   and event.button != 3 and event.button != 4 and event.button != 5:
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
            draw_scoreboard_background(screen, 400, 200)  # Add this line
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
            draw_scoreboard_background(screen, 600, 500)
            menu_buttons, textbox_rect = draw_help_menu(screen, text_input_visualizer_help, events)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    copy_to_clipboard(text_input_manager_help.value)
                elif event.key == pygame.K_v and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    text_input_manager_help.set_text(paste_from_clipboard())
                elif event.key == pygame.K_RETURN:
                    input_text_help = text_input_manager_help.value  # Get the input from the text_input_manager
                    file_path_one = "server.txt"

                    if not os.path.exists(file_path_one):
                        print("server.txt does exist! Do you want to play online?")
                        with open(file_path_one, "w") as f:
                            f.write("")
                            pass  # You can write some initial content here if you want, or just leave it empty
                    with open("server.txt", "r") as f:
                        if not is_valid_ip(f.read()) or is_valid_ip(input_text_help):
                            print("Updating empty IP file with " + input_text_help)
                            with open("server.txt", "w") as f:
                                if (is_valid_ip(input_text_help)):
                                    f.write(input_text_help)  # Update the server.txt file with the input
                    # Update the server_data variable in Network.py
                    Network.server_data = input_text_help # Change this line
                    text_input_manager_help.clear_text()  # Clear the file
        elif game_state == "import":
            draw_transparent_background(screen)
            draw_scoreboard_background(screen, 700, 450)

            menu_buttons, textbox_rect = draw_import_export_menu(screen, text_input_visualizer_import, events)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    copy_to_clipboard(text_input_manager_import.value)
                elif event.key == pygame.K_v and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    text_input_manager_import.set_text(paste_from_clipboard())
                elif event.key == pygame.K_RETURN:
                    input_text_import = text_input_manager_import.value  # Get the input from the text_input_manager

                    with open(file_path_two, "r") as f:
                        if f.read() == "" or input_text_import != "":
                            with open("import.txt", "w") as f:
                                f.write(input_text_import)  # Update the server.txt file with the input
                        if input_text_import != "" and is_valid_import(input_text_import):
                                print("Import is valid. Attempting to setup board.")
                                decoded_moves = decode_import(input_text_import)
                                for move in decoded_moves:
                                    chess_board.move_piece(*move)

                    # Update the server_data variable in Network.py
                    Network.server_data = input_text_import
                    #print(input_text)
                    text_input_manager_import.clear_text() # Clear the input after updating the file

            elif event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                game_state = "menu"

        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    main()