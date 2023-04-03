import pygame

# Define SELECTED_COLOR as a constant, e.g., (255, 255, 0) for yellow
SELECTED_COLOR = (0, 255, 0)

# Constants
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

# Colors
LIGHT_BROWN = (255,206,158,255)
DARK_BROWN =  (209,139,71,255)

# Initialize Pygame
pygame.init()

# Load and resize images
def load_image(file_name):
    image = pygame.image.load(file_name)
    return pygame.transform.scale(image, (SQUARE_SIZE, SQUARE_SIZE))

def load_images():
    global pieces
    pieces = {
        "R": (load_image("images/white_rook.png"), load_image("images/white_rook_dark.png")),
        "N": (load_image("images/white_knight.png"), load_image("images/white_knight_dark.png")),
        "B": (load_image("images/white_bishop.png"), load_image("images/white_bishop_dark.png")),
        "Q": (load_image("images/white_queen.png"), load_image("images/white_queen_dark.png")),
        "K": (load_image("images/white_king.png"), load_image("images/white_king_dark.png")),
        "P": (load_image("images/white_pawn.png"), load_image("images/white_pawn_dark.png")),
        "r": (load_image("images/black_rook.png"), load_image("images/black_rook_dark.png")),
        "n": (load_image("images/black_knight.png"), load_image("images/black_knight_dark.png")),
        "b": (load_image("images/black_bishop.png"), load_image("images/black_bishop_dark.png")),
        "q": (load_image("images/black_queen.png"), load_image("images/black_queen_dark.png")),
        "k": (load_image("images/black_king.png"), load_image("images/black_king_dark.png")),
        "p": (load_image("images/black_pawn.png"), load_image("images/black_pawn_dark.png")),
    }

# Call the load_images function here
load_images()

pieces = {
    "R": load_image("images/white_rook.png"),
    "N": load_image("images/white_knight.png"),
    "B": load_image("images/white_bishop.png"),
    "Q": load_image("images/white_queen.png"),
    "K": load_image("images/white_king.png"),
    "P": load_image("images/white_pawn.png"),
    "r": load_image("images/black_rook.png"),
    "n": load_image("images/black_knight.png"),
    "b": load_image("images/black_bishop.png"),
    "q": load_image("images/black_queen.png"),
    "k": load_image("images/black_king.png"),
    "p": load_image("images/black_pawn.png")
}

def import_export_function():
    # Add import/export functionality here
    pass

def help_function():
    # Add help functionality here
    pass

def draw_transparent_background(screen):
    TRANSPARENT_COLOR = (0, 0, 0, 128)
    surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    surf.fill(TRANSPARENT_COLOR)
    screen.blit(surf, (0, 0))

def draw_menu(screen, menu_state):
    #sprint("draw_menu function used")
    MENU_WIDTH, MENU_HEIGHT = 600, 400
    MENU_COLOR = (153, 102, 51)
    MENU_BORDER_COLOR = (0, 0, 0)
    menu_rect = pygame.Rect((WIDTH - MENU_WIDTH) // 2, (HEIGHT - MENU_HEIGHT) // 2, MENU_WIDTH, MENU_HEIGHT)
    pygame.draw.rect(screen, MENU_COLOR, menu_rect)
    pygame.draw.rect(screen, MENU_BORDER_COLOR, menu_rect, 5)
    menu_buttons = []
    if menu_state == "main":
        menu_buttons = draw_main_menu(screen)
    return menu_buttons

def draw_main_menu(screen):
    menu_buttons = [
        {"text": "Resume", "function": "resume"},
        {"text": "Scoreboard", "function": "scoreboard"},
        {"text": "Help", "function": "help"},
        {"text": "Import/Export", "function": "import_export"}
    ]

    button_width, button_height = 200, 50  # Increase button width for "Import/Export"
    button_margin = 20
    button_start_y = ((HEIGHT - sum([button_height + button_margin for _ in menu_buttons]) - button_margin) // 2) + 20

    for i, button in enumerate(menu_buttons):
        button_x = (WIDTH - button_width) // 2
        button_y = button_start_y + (button_height + button_margin) * i
        button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        pygame.draw.rect(screen, (128, 128, 128), button_rect)
        pygame.draw.rect(screen, (0, 0, 0), button_rect, 2)

        font = pygame.font.Font(None, 36)
        text_surf = font.render(button["text"], True, (0, 0, 0))
        text_rect = text_surf.get_rect()
        text_rect.center = button_rect.center
        screen.blit(text_surf, text_rect)

        button["rect"] = button_rect

    return menu_buttons

def draw_scoreboard(screen, chess_board):
    font = pygame.font.Font(None, 36)
    score = chess_board.get_score()
    white_score_text = f"White: {score['white']}"
    black_score_text = f"Black: {score['black']}"

    white_score_pos = (WIDTH // 2 - font.size(white_score_text)[0] // 2, HEIGHT // 2 - 50)
    screen.blit(font.render(white_score_text, True, (0, 0, 0)), white_score_pos)

    black_score_pos = (WIDTH // 2 - font.size(black_score_text)[0] // 2, HEIGHT // 2 + 20)
    screen.blit(font.render(black_score_text, True, (0, 0, 0)), black_score_pos)

# Function to handle graphical board display
def draw_board(screen, chess_board, selected_piece=None):
    BORDER_WIDTH = 4  # Width of the border around the selected square
    BORDER_COLOR = SELECTED_COLOR  # Yellow color for the border

    for row in range(ROWS):
        for col in range(COLS):
            color = LIGHT_BROWN if (row + col) % 2 == 0 else DARK_BROWN
            pygame.draw.rect(screen, color, pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

            piece = chess_board.get_piece(row, col)
            if piece != ' ':
                image_idx = 0 if (row + col) % 2 == 0 else 1  # Use the light image for light squares and dark image for dark squares
                screen.blit(pieces[piece][image_idx], (col * SQUARE_SIZE, row * SQUARE_SIZE))

            if selected_piece and (row, col) == selected_piece:
                pygame.draw.rect(screen, BORDER_COLOR, pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), BORDER_WIDTH)