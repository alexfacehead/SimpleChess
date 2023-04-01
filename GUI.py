import pygame
from ChessBoard import ChessBoard

# Constants
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

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

# Function to handle graphical board display
def draw_board(screen, chess_board):
    for row in range(ROWS):
        for col in range(COLS):
            color = WHITE if (row + col) % 2 == 0 else BLACK
            pygame.draw.rect(screen, color, pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

            piece = chess_board.get_piece(row, col)
            if piece != ' ':
                screen.blit(pieces[piece], (col * SQUARE_SIZE, row * SQUARE_SIZE))