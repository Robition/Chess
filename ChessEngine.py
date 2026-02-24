# This is where the data will be STORED, for storing all info about the
# 'state' of the chess game. It'll also handle move logic, and it'll keep track of moves.

# The constant state of the board.
class GameState:
    def __init__(self):
        # List in a list, to represent the board for ease of use later on.
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        self.whiteToMove = True
        self.movelog = []



    # To make a general move, we need the initial position, and the end position. With board of course.
    # When moving a piece, there's two things that happen:
    # 1. The piece leaves its original spot (making it empty)
    # 2. The piece takes the space of the end move (so end is now where the piece is)
    def makeMove(self, move):
        if self.board[move.startRow][move.startCol] != "--": # Making sure that a piece was selected
            self.board[move.startRow][move.startCol] = "--"
            self.board[move.endRow][move.endCol] = move.pieceMoved
            self.movelog.append(move) # Storing the reference to the objects instnce
            self.whiteToMove = not self.whiteToMove

    # To undo a move:
    # I have the move history stored already. I need to just read that input, pop it off
    def undoMove(self):
        if self.movelog != 0:
            move = self.movelog.pop() # Temp list var for the move just removed
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove

    def getValidMoves(self):
        return

    '''
    To consider all moves:
    Go through the board and find all of the pieces (nested loop)
    Check to know who's turn it is
    Access each pieces logic
    Calculate all moves for each piece (And store it)
    '''
    def getAllMoves(self):
        moves = [] # List to store moves
        for rows in range(len(self.board)): # How many rows there are (8)
            for cols in range(len(self.board[rows])): # Counts how many cols there are in each row (8)
                piece_color = self.board[rows][cols][0] # [w]P
                if(piece_color == 'w' and self.whiteToMove) and (piece_color == 'b' and not self.whiteToMove): # Find each piece for the players turn
                    piece = self.board[rows][cols][1] # w[P]
                    if piece == 'P':
                        self.getPawnMoves(rows, cols, moves)
                    if piece == 'R':
                        self.getRookMoves(rows, cols, moves)

    # Returns all possible
    def getPawnMoves(self, rows, cols, moves):
        pass

    def getRookMoves(self, rows, cols, moves):
        pass


class Move:

    # key : value
    # Top left is zero in list, but its 8 in chess notation
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}

    # value : key
    # Seperately grabs both values in the tuple, then at the end
    # of each iteration, flips the 'key' (k) and 'value' (v)
    rowsToRanks = {v: k for k, v in ranksToRows.items()}

    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        
    def getChessNotation(self):
        """
        Algebraic notation Symbols for later usage
        TODO: FEN notation
        x -> Piece taken
        e.p. -> Piece taken en passant
        + -> Check
        # -> Checkmate
        = -> Pawn promotion *
        0-0 -> Castle King-side
        0-0-0 -> Castle Queen-side
        1-0 -> White win
        ½-½ -> Draw
        0-1 -> Black win
        (=) -> Draw offered
        """
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    # Helper function to return the Rank + File in chess notation
    # Tempted to make this a class method just for the practice lol
    def getRankFile(self, row, col):
        return self.colsToFiles[col] + self.rowsToRanks[row]
