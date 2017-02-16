board = [["?"] * 10 for i in range(0,11)]
rowTents = {0: 2, 9:1}
colTents = {2: 2, 9:1}
board[2][2] = "O"
board[0][2] = "O"
board[2][3] = "X"
board[2][4] = "O"
board[10][0] = "X"

def printBoard():
    border = "************"
    print(border)
    for row in board:
        toPrint = ""
        for col in row:
            toPrint += col
        print("*" + toPrint + "*")
    print(border)

def isValidSum(x,y):
    totalRowTents = 1
    totalColTents = 1

    for col in board[x]:
        if col == "O":
            totalRowTents += 1
    if(totalRowTents > rowTents[x]):
        return False

    for i in range(0, len(board)):
        if board[i][y] == "O":
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

def getNonAdjGrass():
    print(len(board[0]))
    print(len(board))
    for row in range(0,len(board)):
        for col in range(0, len(board[0])):
            if(board[row][col] != "O"):
                board[row][col] = "."
                for each in getNeighbors(row, col):
                    print(row, col, each)
                    if(board[each[0]][each[1]] == "O"):
                        board[row][col] = "?"
                        break

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

#getNonAdjGrass()
printBoard()
print(isValidParity(1,2))
print(noAdjTents(0,0))
print(isValidSum(0,2))