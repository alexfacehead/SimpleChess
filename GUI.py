import pygame
from ChessBoard import ChessBoard

# Define SELECTED_COLOR as a constant, e.g., (255, 255, 0) for yellow
SELECTED_COLOR = (0, 0, 255)

# Constants
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

# Colors
LIGHT_BROWN = (245, 222, 179)
DARK_BROWN = (139, 69, 19)

# Initialize Pygame
pygame.init()

# Load and resize images
def load_image(file_name):
    image = pygame.image.load(file_name)
    return pygame.transform.scale(image, (SQUARE_SIZE, SQUARE_SIZE))

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

def draw_menu(screen):
    MENU_WIDTH, MENU_HEIGHT = 200, 600
    MENU_COLOR = (128, 128, 128)
    menu_rect = pygame.Rect(WIDTH, 0, MENU_WIDTH, MENU_HEIGHT)
    pygame.draw.rect(screen, MENU_COLOR, menu_rect)
    # Add more menu elements here as needed

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
                screen.blit(pieces[piece], (col * SQUARE_SIZE, row * SQUARE_SIZE))

            if selected_piece and (row, col) == selected_piece:
                pygame.draw.rect(screen, BORDER_COLOR, pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), BORDER_WIDTH)