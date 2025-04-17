
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

    """
    takes a parameter (move) and executes the move on the board (beta version) because can eat its own pieces
    """
    def make_move(self, move):
        print(f"Making move: {move.getNotation()}")
        self.board[move.startRow][move.startCol] = "--" # empty the start square
        self.board[move.endRow][move.endCol] = move.pieceMove # move the piece to the end square
        self.move_log.append(move)# add the move to the move log so we can undo like in chess or record history of game
        self.white_to_move = not self.white_to_move # switch turns

    """
    Undo the last move 
    """
    def undo_move(self):
        if len(self.move_log) != 0: #Cant undo if its empty no move has been done
            move = self.move_log.pop()
            self.board[move.startRow][move.startCol] = move.pieceMove # put the piece back to the start square
            self.board[move.endRow][move.endCol] = move.pieceEnd # put the piece back to the end square
            self.white_to_move = not self.white_to_move # switch turns back to the original player

    #This in a real tournament wont be accepable but for testing purposes is ok

    """
    All moves While king in check
    """
    def getValidMoves(self):
        return self.getAllPossibleMoves() # get all possible moves without worrying about the king in check for now


    """
    All legal moves without king in check
    """
    def getAllPossibleMoves(self):
        moves = []
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                #In a 2d self.board[0] will give us the len of the rows but we need the len of the col in a given row
                turn = self.board[row][col][0] #we will get the given sq on the board and its given color (W or B)
                if (turn == "w" and self.white_to_move) or (turn == "b" and not self.white_to_move):
                    piece = self.board[row][col][1] #gives the piece type
                    if piece == "P":
                        self.getPawnMoves(row, col, moves)
                    elif piece == "R":
                        self.getRookMoves(row, col, moves)
                    elif piece == "N":
                        self.getKnightMoves(row, col, moves)
                    elif piece == "B":
                        self.getBishopMoves(row, col, moves)
                    elif piece == "Q":
                        self.getQueenMoves(row, col, moves)
                    elif piece == "K":
                        self.getKingMoves(row, col, moves)

                    #Might do a caller functions instead all the if statements to make it more readable aesthetic 

        return moves


    """
    Functions for each individual piece row, col and moves to the list
    """
    def getPawnMoves(self, row, col, moves):
        if self.white_to_move:
            if self.board[row - 1][col] == "--":
                moves.append(Move((row, col), (row - 1, col), self.board))
                if row == 6 and self.board[row - 2][col] == "--":
                    moves.append(Move((row, col), (row - 2, col), self.board))

            if col - 1 >= 0: #Capture left enemy
                if self.board[row - 1][col - 1][0] == "b":
                    moves.append(Move((row, col), (row - 1, col - 1), self.board))
            if col + 1 <= 7: # capture right enemy
                if self.board[row - 1][col + 1][0] == "b":
                    moves.append(Move((row, col), (row - 1, col + 1), self.board))

        else: #black pawn move
            if self.board[row + 1][col] == "--":
                moves.append((Move((row, col),(row + 1, col), self.board)))
                if row == 1 and self.board[row + 2][col] == "--":
                    moves.append(Move((row, col), (row + 2, col), self.board))

            if col - 1 >= 0: # Cupture left enemy
                if self.board[row + 1][col - 1][0] == "w":
                    moves.append(Move((row, col), (row + 1, col - 1), self.board))
            if col + 1 <= 7:
                if self.board[row + 1][col + 1][0] == "w":
                    moves.append(Move((row, col), (row + 1, col + 1), self.board))


    def getRookMoves(self, row, col, moves):
        directions = ((1, 0), (-1, 0), (0, 1), (0, -1))
        enemy_color = "b" if self.white_to_move else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = row + d[0] * i
                endCol = col + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((row, col), (endRow, endCol), self.board))
                    elif endPiece[0] == enemy_color:
                        moves.append(Move((row, col), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break

    def getKnightMoves(self, row, col, moves):
        directions = ((2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2))
        enemy_color = "b" if self.white_to_move else "w"
        for d in directions:
            endRow = row + d[0]
            endCol = col + d[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece != enemy_color: # if the piece is not the same color not an ally piece
                    moves.append(Move((row, col), (endRow, endCol), self.board))


    def getBishopMoves(self, row, col, moves):
        directions = ((1, 1), (1, -1), (-1, 1), (-1, -1))
        enemy_color = "b" if self.white_to_move else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = row + d[0] * i
                endCol = col + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((row, col), (endRow, endCol), self.board))
                    elif endPiece[0] == enemy_color:
                        moves.append(Move((row, col), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break


    def getQueenMoves(self, row, col, moves):
        directions = ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1))
        enemy_color = "b" if self.white_to_move else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = row + d[0] * i
                endCol = col + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((row, col), (endRow, endCol), self.board))
                    elif endPiece[0] == enemy_color:
                        moves.append(Move((row, col), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break
        #Might be a bit redundant but is ok for now like leetcode 51.N queens problem
        #Should be easier implementation of the queen moves and not that messy


    def getKingMoves(self, row, col, moves):
        directions = ((1, 0), (-1, 0 ), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1))
        enemy_colro = "b" if self.white_to_move else "w"
        for i in range(8):
            endRow = row + directions[i][0]
            endCol = col + directions[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != enemy_colro:
                    moves.append(Move((row, col), (endRow, endCol), self.board))

        #did modify it because forgot the logic of castling haha will do it in a bit






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
        self.MoveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
        #Just a way to identify the move in a unique way so we can get the move 0000 - 7777
        #For example 0002 is from (row 0 col) 0 to (row 0 col 2)
        #print(self.MoveID)

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.MoveID == other.MoveID
        return False

    def getNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.cols_as_alphabet[c] + self.rows_as_numbers[r]
        #We do it as for In chess we need to make alphabet first the numeric second like a8,b7,c6,d5 etc...
