import pygame as p
from Chess import ChessEngine


WIDTH, HEIGHT = 512,512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

def load_images():
    pieces = ['wK', 'wN', 'wB', 'wQ', 'wR', 'wP', 'bK', 'bN', 'bB', 'bQ', 'bR', 'bP']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
    # Load images for the chess pieces

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.Game()
    load_images()
    running = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
        draw_game(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()

def draw_game(screen, gs):
    draw_board(screen)
    draw_pieces(screen, gs.board)

def draw_board(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            color = colors[(row + col) % 2]
            p.draw.rect(screen, color, p.Rect(col * SQ_SIZE , row * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def draw_pieces(screen, board):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = board[row][col]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == "__main__":
    main()