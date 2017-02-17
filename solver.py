import copy

board = [["?"] * 6 for i in range(0,6)]
rowTents = {0:2, 1:1, 2:1, 3:1, 4:1, 5:1}
colTents = {0:1, 1:2, 2:1, 3:1, 4:2, 5:0}
board[0][1] = "O"
board[1][0] = "O"
board[2][2] = "O"
board[2][4] = "O"
board[3][4] = "O"
board[4][2] = "O"
board[4][4] = "O"

def init():
    f = open("tents.txt","r")
    for line in f:
        print(line)

def printBoard():
    border = "**" + "*"*len(board[0])
    print(border)
    for row in board:
        toPrint = ""
        for col in row:
            toPrint += col
        print("*" + toPrint + "*")
    print(border)

def isValid(row,col):
    if(isValidSum(row, col) and isValidParity(row,col) and noAdjTents(row, col)):
        return True
    return False

def isValidSum(x,y):
    totalRowTents = 1
    totalColTents = 1

    for col in board[x]:
        if col == "X":
            totalRowTents += 1
    if(totalRowTents > rowTents[x]):
        return False

    for i in range(0, len(board)):
        if board[i][y] == "X":
            totalColTents += 1
    if(totalColTents > colTents[y]):
        return False
    return True

def isValidParity(x,y):
    parity = -1
    pred = [(x,y)]
    for each in getNeighbors(x,y):
        parity += countTreesRec(each[0], each[1], pred)

    if(parity >= 0):
        return True
    else:
        return False

def countTreesRec(x,y, pred):
    pred += [(x,y)]
    if(board[x][y] == "O"):
        parity = 1
        for each in getNeighbors(x,y):
            if(each not in pred):
                parity += countTentsRec(each[0],each[1], pred)
        return parity
    else:
        return 0

def countTentsRec(x,y, pred):
    pred += [(x,y)]
    if (board[x][y] == "X"):
        parity = -1
        for each in getNeighbors(x, y):
            if (each not in pred):
                parity += countTreesRec(each[0], each[1], pred)
        return parity
    else:
        return 0

def getNeighbors(x,y):
    neighbors = []
    if(x > 0):
        neighbors += [(x-1,y)]
    if(x < len(board) - 1):
        neighbors += [(x+1, y)]
    if(y > 0):
        neighbors += [(x,y-1)]
    if(y < len(board[x])-1):
        neighbors += [(x, y+1)]
    return neighbors

def noAdjTents(x,y):
    for each in getNeighbors(x,y):
        if(board[each[0]][each[1]] == "X"):
            return False
    if(x > 0 and y > 0):
        if(board[x-1][y-1] == "X"):
            return False

    if (x > 0 and y < len(board[x]) - 1):
        if (board[x-1][y+1] == "X"):
            return False

    if (x < len(board) - 1 and y > 0):
        if (board[x+1][y-1] == "X"):
            return False

    if (x < len(board) - 1 and y < len(board[x]) - 1):
        if (board[x+1][y+1] == "X"):
            return False

    return True


def getNonAdjGrass():
    for row in range(0,len(board)):
        for col in range(0, len(board[0])):
            if(board[row][col] != "O"):
                board[row][col] = "."
                for each in getNeighbors(row, col):
                    if(board[each[0]][each[1]] == "O"):
                        board[row][col] = "?"
                        break

def findUnknown():
    for row in range(0, len(board)):
        for col in range(0, len(board[row])):
            if(board[row][col] == "?"):
                return (row,col)

    return None

def solve():
    getNonAdjGrass()
    if(findUnknown() != None):
        row, col = findUnknown()
        return solveRec(row, col)
    else:
        if(isGoal()):
            return True
        else:
            return None

def solveRec(row, col):
    print("------------------------")
    printBoard()
    metadata = saveMetadata()
    if(isValid(row,col)):
        board[row][col] = "X"
        if (findUnknown() != None):
            row, col = findUnknown()
            if(solveRec(row, col) == True):
                return True
            else:
                restoreMetadata(metadata)
                board[row][col] = "."
                if (solveRec(row, col) == True):
                    return True
                else:
                    return None
        else:
            if(isGoal()):
                return True
            else:
                return None
    else:
        board[row][col] = "."
        if(findUnknown() != None):
            row, col = findUnknown()
            if (solveRec(row, col) == True):
                return True
            else:
                return None
        else:
            if(isGoal()):
                return True
            else:
                return None

def isGoal():
    totalRowTents = 0
    totalColTents = 0

    for row in range(0, len(board)):
        for col in range(0, len(board[0])):
            if board[row][col] == "X":
                totalRowTents += 1
        if (totalRowTents != rowTents[row]):
            return False
        else:
            totalRowTents = 0

    for col in range(0, len(board[0])):
        for row in range(0, len(board)):
            if board[row][col] == "X":
                totalColTents += 1
        if (totalColTents != colTents[col]):
            return False
        else:
            totalColTents = 0

        return True


def saveMetadata():
    return (copy.deepcopy(board),
            copy.deepcopy(rowTents),
            copy.deepcopy(colTents))

def restoreMetadata(metadata):
    global board, rowTents, colTents
    board,rowTents,colTents = metadata

#print(solve())
#printBoard()
#print(isGoal())