import pygame as p
from Chess import ChessEngine

WIDTH, HEIGHT = 512, 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

def load_images():
    pieces = ['wK', 'wN', 'wB', 'wQ', 'wR', 'wP', 'bK', 'bN', 'bB', 'bQ', 'bR', 'bP']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.Game()
    validMoves = gs.getValidMoves() #after a player does a move we can see if its valid or not
    moveMade = False #Flag for when a move is made just after the player makes a move we call the getValidMoves
    #to see the generated valid moves after a move is made not before (not to overkill the engine)
    load_images()
    running = True
    sq_selected = () #for storing the last click of the user
    player_clicks = [] #for storing the last two clicks of the user for the move
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN: # when the user clicks the mouse
                location = p.mouse.get_pos()  # get the position of the mouse click
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if sq_selected == (row, col):# if the user clicks the same square again
                    sq_selected = () # deselect the square
                    player_clicks = [] # reset the clicks
                else:
                    sq_selected = (row, col)
                    player_clicks.append(sq_selected)
                if len(player_clicks) == 2: # if the user has clicked two squares
                    move = ChessEngine.Move(player_clicks[0], player_clicks[1], gs.board)
                    print(move.getNotation())
                    if move in validMoves:
                        gs.make_move(move)
                        moveMade = True

                    gs.make_move(move) # make the move
                    sq_selected = () # reset the square
                    player_clicks = [] # reset the clicks


            #Keyboard events for Undoing the move
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: #Undo the move when z is pressed
                    gs.undo_move()
                    moveMade = True


        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False

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
            p.draw.rect(screen, color, p.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def draw_pieces(screen, board):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = board[row][col]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))

if __name__ == "__main__":
    main()
