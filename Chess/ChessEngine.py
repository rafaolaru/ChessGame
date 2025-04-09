


class Game():
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.white_to_move = True
        self.move_log = []

    def make_move(self, move):
        print(f"Making move: {move.getNotation()}")
        self.board[move.startRow][move.startCol] = "--" # empty the start square
        self.board[move.endRow][move.endCol] = move.pieceMove # move the piece to the end square
        self.move_log.append(move)# add the move to the move log so we can undo like in chess or record history of game
        self.white_to_move = not self.white_to_move # switch turns
class Move():


    numbering_the_rows = {"1" : 7, "2" : 6, "3" : 5, "4" : 4, "5" : 3, "6" : 2, "7" : 1, "8" : 0}

    rows_as_numbers = {v: k for k, v in numbering_the_rows.items()} # reverse the dictionary

    alphabet_the_cols = {"a" : 0, "b" : 1, "c" : 2, "d" : 3, "e" : 4, "f" : 5, "g" : 6, "h" : 7}

    cols_as_alphabet = {v: k for k, v in alphabet_the_cols.items()} # reverse the dictionary

    def __init__(self, start, end, board):
        self.startRow = start[0]
        self.startCol = start[1]
        self.endRow = end[0]
        self.endCol = end[1]
        self.pieceMove = board[self.startRow][self.startCol]
        self.pieceEnd = board[self.endRow][self.endCol]

    def getNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.cols_as_alphabet[c] + self.rows_as_numbers[r]
        #We do it as for In chess we need to make alphabet first the numeric second like a8,b7,c6,d5 etc...
