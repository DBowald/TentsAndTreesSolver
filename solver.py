import copy
import sys

board = []
rowTents = {}
colTents = {}

def init():
    global rowTents, colTents, board
    f = open(sys.argv[1],"r")
    count = 0
    f.readline()
    line = f.readline().strip().split("x")
    board = [["?"] * int(line[1]) for i in range(0,int(line[0]))]
    f.readline()
    while(True):
        line = f.readline().strip()
        if(line == "Columns"):
            break
        else:
            rowTents[count] = int(line)
            count += 1
    count = 0
    while (True):
        line = f.readline().strip()
        if (line == "Trees"):
            break
        else:
            colTents[count] = int(line)
            count += 1
    while(True):
        line = f.readline().strip()
        if(line == ""):
            break
        else:
            line = line.split(",")
            board[int(line[0])][int(line[1])] = "O"
    f.close()

def printBoard():
    border = "  * * " + "* "*len(board[0])
    count = 0
    bottom = ""
    print(border)
    for row in board:
        toPrint = ""
        for col in row:
            toPrint += col + " "
        print(str(rowTents[count]) + " * " + toPrint + "*")
        bottom += str(colTents[count]) + " "
        count += 1
    print(border)
    print("    " + bottom + " ")



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

def getTentAdjacent(x,y):
    neighbors = getNeighbors(x,y)
    if (x > 0 and y > 0):
        neighbors += [(x-1,y-1)]
    if (x > 0 and y < len(board[x]) - 1):
        neighbors += [(x-1, y+1)]
    if (x < len(board) - 1 and y > 0):
        neighbors += [(x+1, y-1)]
    if (x < len(board) - 1 and y < len(board[x])- 1):
        neighbors += [(x+1, y+1)]

    return neighbors

def noAdjTents(x,y):
    for each in getTentAdjacent(x,y):
        if(board[each[0]][each[1]] == "X"):
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

def markTentAdjGrass(x,y):
    for each in getTentAdjacent(x, y):
        if (board[each[0]][each[1]] != "O"):
            board[each[0]][each[1]] = "."

def markNonBranching():
    totalRowOccupants = 0
    totalColOccupants = 0

    for row in range(0, len(board)):
        for col in range(0, len(board[0])):
            print(totalRowOccupants)
            if board[row][col] == "O" or board[row][col] == ".":
                totalRowOccupants += 1
            if(rowTents[row] == 0 and board[row][col] != "O"):
                board[row][col] = "."
        if (len(board[0]) - totalRowOccupants == rowTents[row]):
            for j in range(0, len(board[0])):
                if(board[row][j] == "?"):
                    board[row][j] = "X"
        totalRowOccupants = 0

    for col in range(0, len(board[0])):
        for row in range(0, len(board)):
            if (board[row][col] == "O" or board[row][col] == "."):
                totalColOccupants += 1
            if (colTents[col] == 0 and board[row][col] != "O"):
                board[row][col] = "."
        if (len(board) - totalColOccupants == colTents[col]):
            for i in range(0, len(board)):
                if (board[i][col] == "?"):
                    board[i][col] = "X"
        totalColOccupants = 0

def findUnknown():
    for row in range(0, len(board)):
        for col in range(0, len(board[row])):
            if(board[row][col] == "?"):
                return (row,col)

    return None

def solve():
    getNonAdjGrass()
    markNonBranching()
    markNonBranching()
    if(findUnknown() != None):
        row, col = findUnknown()
        return solveRec(row, col)
    else:
        if(isGoal()):
            return True
        else:
            return None

def solveRec(row, col):
    #print("------------------------")
    #printBoard()
    metadata = saveMetadata()
    if(isValid(row,col)):
        board[row][col] = "X"
        markTentAdjGrass(row, col)
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

init()
print(solve())
printBoard()

printBoard()
#print(isGoal())
