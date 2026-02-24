# Main 'driver' file, this is where user input and where
# displaying GameState Object will occur.

import pygame as p
from Chess import ChessEngine

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}
colors = ["w", "b"]
pieces = ["P", "R", "N", "B", "Q", "K"]

# Load images only once -- This will initialize a global dict of the images
def loadImages():
    # Automate the loading of images
    for color in colors:
        for piece in pieces:
            IMAGES[color + piece] = p.transform.scale(p.image.load(f'images/{color + piece}.png'), (SQ_SIZE, SQ_SIZE))

# Main driver: Handles user input and updating graphics
def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validmoves = gs.getValidMoves() # Returns a list of all VALID moves in initial state
    movestate = False # We want to check for NEW valid moves after we move a piece
    loadImages() # Only done once
    running = True
    sqselected = () # Keeps track of users square clicked
    playerclicks = [] # Two tuples, one for each click spot location (x,y)

    while running: # Per-frame updates - things that happen every frame
        # Not everything needs to be inside the event. Only stuff that requires constant input checking
        for event in p.event.get(): # event used for getting mouse clicks and mouse positioning
            if event.type == p.QUIT:
                running = False
            elif event.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sqselected == (row, col): # They selected the same piece (unclicking)
                    sqselected = ()
                    playerclicks = []
                else:
                    sqselected = (row, col)
                    playerclicks.append(sqselected)

                if len(playerclicks) == 2:
                    move = ChessEngine.Move(playerclicks[0], playerclicks[1] , gs.board) # ONLY place we need to check the boards state.
                    if move in validmoves: # Checks if the current move is stored in validMoves list when we check.
                        gs.makeMove(move)
                        movestate = True # Success! Move worked. Now we need to update the new valid moves.
                    playerclicks = []
            elif event.type == p.KEYDOWN:
                if event.key == p.K_r:
                    gs.undoMove()
                    playerclicks = []
                    sqselected = ()
                    movestate = True
        if movestate: # Has the moveState changed? Okay now we need updated valid moves
            validmoves = gs.getValidMoves()
            movestate = False

        drawGameState(screen, gs, sqselected)
        clock.tick(MAX_FPS)
        p.display.flip()



# Draws all graphics in current game state
def drawGameState(screen, gs, sqselected):
    drawBoard(screen, sqselected) # This needs to be constantly refreshed so that we don't have duplicates on a board, keeps it up to date
    drawPieces(screen, gs.board)


def drawBoard(screen, sqselected):
    # Start at 0,0 and expand right, using SQ_SIZE for location iteration and dimension as the col and row iterator
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            if (row, col) == sqselected:
                p.draw.rect(screen, p.Color("Yellow"), p.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))
            elif (row + col) % 2 == 0:
                p.draw.rect(screen, p.Color("Gray"), p.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))
            else:
                p.draw.rect(screen, p.Color("Dark Green"), p.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawPieces(screen, board):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            if board[row][col] != "--":
                screen.blit(IMAGES[board[row][col]], (col * SQ_SIZE, row * SQ_SIZE))

if __name__ == "__main__":
    main()