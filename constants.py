import pygame


WIDTH, HEIGHT = 1200, 1500
BOARD_OFFSET = 100
BOARD_WIDTH, BOARD_HEIGHT = 1000, 1000
ROWS, COLS = 8, 8
SQUARE_SIZE = BOARD_WIDTH//COLS

#  Colour scheme (RGB)

MAHOGANY = (120, 76, 45) 
PASTEL = (233, 195, 167)

WHITE = (248, 235, 226)
BLACK = (37, 27, 26)

ALLIGATOR = (83, 57, 46) 
BLUE = (0, 0, 255)

#  IMAGE ASSETS
TITLE = pygame.image.load('assets/title.png')
TITLE_CARD = pygame.image.load('assets/title-card.png')
BOARD_FRAME = pygame.transform.scale(pygame.image.load('assets/board-frame.png'), (BOARD_WIDTH + BOARD_OFFSET*2, BOARD_HEIGHT + BOARD_OFFSET*2))
BOARD = pygame.transform.scale(pygame.image.load('assets/board.png'), (BOARD_WIDTH, BOARD_HEIGHT))
BOARD_SQUARE = pygame.transform.scale(pygame.image.load('assets/board-square.png'), (SQUARE_SIZE, SQUARE_SIZE))
WHITE_PIECE = pygame.transform.scale(pygame.image.load('assets/white.png'), (SQUARE_SIZE - SQUARE_SIZE//4, SQUARE_SIZE- SQUARE_SIZE//4))
BLACK_PIECE = pygame.transform.scale(pygame.image.load('assets/black.png'), (SQUARE_SIZE - SQUARE_SIZE//4, SQUARE_SIZE- SQUARE_SIZE//4))
WHITE_KING = pygame.transform.scale(pygame.image.load('assets/white-king.png'), (SQUARE_SIZE - SQUARE_SIZE//4, SQUARE_SIZE- SQUARE_SIZE//4))
BLACK_KING = pygame.transform.scale(pygame.image.load('assets/black-king.png'), (SQUARE_SIZE - SQUARE_SIZE//4, SQUARE_SIZE- SQUARE_SIZE//4))