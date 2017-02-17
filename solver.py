"""
AUTHOR: Dylan Bowald

Read the README for a project overview!

Since I kind of awkwardly did this in one file
(it ended up being a lot longer than I thought),
I went ahead and seperated it into sections for
reader convenience.
"""

import copy
import sys

board = []
rowTents = {}
colTents = {}
rowCount = {}
colCount = {}

#####################################################################
# INITIALIZATION AND REPRESENTATION
#####################################################################

"""
Initializes the global board object based on the given file
"""
def init():
    global rowTents, colTents, board
    f = open(sys.argv[1],"r")
    count = 0
    f.readline()
    line = f.readline().strip().split("x")
    board = [["?"] * int(line[1]) for i in range(0,int(line[0]))]
    for each in range(0, len(board)):
        rowCount[each] = 0
        colCount[each] = 0
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

"""Displays the ascii graphic representing the global game board"""
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

#####################################################################
# VALIDITY CHECKING
#####################################################################

"""Checks whether a move at <row, col> is valid within the rules
of tents and trees"""
def isValid(row,col):
    if(isValidSum(row, col) and isValidParity(row,col) and noAdjTents(row, col)):
        return True
    return False

"""Checks whether placing a tent at <row,col> would exceed any of
the given row or column numbers"""
def isValidSum(x,y):
    if(rowCount[x] + 1 > rowTents[x]):
        return False
    if(colCount[y] + 1 > colTents[y]):
        return False
    return True

"""Checks the parity of trees to tents. Essentially, it moves
between a connected chain of tent/tree pairs, and makes sure at
the end the number of trees matches the number of tents"""
def isValidParity(x,y):
    parity = -1
    pred = [(x,y)]
    for each in getNeighbors(x,y):
        parity += countTreesRec(each[0], each[1], pred)

    if(parity >= 0):
        return True
    else:
        return False

"""
Helper function for isValidParity. Called on a tent
to check for any trees around it, and recursively return the tree
to tent parity.
"""
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

"""
Helper function for isValidParity. Called on a tree to
check for any tents around it, and recursively return the tree
to tent parity.
"""
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

"""
Check that there are no tents adjacent to a given location
"""
def noAdjTents(x,y):
    for each in getTentAdjacent(x,y):
        if(board[each[0]][each[1]] == "X"):
            return False

    return True

#####################################################################
# HELPER FUNCTIONS
#####################################################################

"""
Get the vertical and horizontal neighbors at a given
grid coordinate, returned as a list of coordinates.
"""
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

"""
Get the vertical, horizontal, and diagonal neighbors at a given
grid coordinate, returned as a list of coordinates.
"""
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

"""
Polls for an unknown space, and if it finds one,
returns it as a coordinate.
"""
def findUnknown():
    for row in range(0, len(board)):
        for col in range(0, len(board[row])):
            if(board[row][col] == "?"):
                return (row,col)

    return None

"""
Checks the board against the game constraints
to see whether or not we have reached a goal
state. Returns true if so, false otherwise.
"""
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

    """
    Returns a deepcopy of all the global state.
    """

def saveMetadata():
    return (copy.deepcopy(board),
            copy.deepcopy(rowTents),
            copy.deepcopy(colTents),
            copy.deepcopy(rowCount),
            copy.deepcopy(colCount))

"""
Assigns the global state to a given tuple of metadata.
"""

def restoreMetadata(metadata):
    global board, rowTents, colTents, rowCount, colCount
    board, rowTents, colTents, rowCount, colCount = metadata

#####################################################################
# STRATEGIES
#####################################################################

"""
Mark any spaces not adjacent to a tree as grass
"""
def getNonAdjGrass():
    for row in range(0,len(board)):
        for col in range(0, len(board[0])):
            if(board[row][col] != "O"):
                board[row][col] = "."
                for each in getNeighbors(row, col):
                    if(board[each[0]][each[1]] == "O"):
                        board[row][col] = "?"
                        break

"""
Marks any spaces adjacent to a placed tent as grass
"""
def markTentAdjGrass(x,y):
    for each in getTentAdjacent(x, y):
        if (board[each[0]][each[1]] != "O"):
            board[each[0]][each[1]] = "."

"""
Checks the row and column numbers, then marks
any rows or columns with a 0 as grass. Also
checks to see if any of them have the same number
of open spaces as tents needed, and if they do, fills
in those spaces with tents.
"""
def markNonBranching():
    totalRowOccupants = 0
    totalColOccupants = 0

    for row in range(0, len(board)):
        for col in range(0, len(board[0])):
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

"""
Checks the given row and column numbers, then
checks to see if they have the same number
of open spaces as tents needed, and if they do,
fills n those spaces with tents. Compares number
of tents to row and column numbers, and if equal,
fills in the rest of the spaces with grass.
"""
def markTentRowCol(x,y):
    totalRowOccupants = 0
    totalColOccupants = 0

    for col in range(0, len(board[0])):
        if board[x][col] == "O" or board[x][col] == "." or board[x][col] == "X":
            totalRowOccupants += 1
    if (len(board[0]) - totalRowOccupants == rowTents[x]):
        for j in range(0, len(board[0])):
            if(board[x][j] == "?"):
                board[x][j] = "X"
    if(rowTents[x] == rowCount[x]):
        for j in range(0, len(board[0])):
            if(board[x][j] == "?"):
                board[x][j] = "."

    for row in range(0, len(board)):
        if (board[row][y] == "O" or board[row][y] == "." or board[row][y] == "X"):
            totalColOccupants += 1
    if (len(board) - totalColOccupants == colTents[col]):
        for i in range(0, len(board)):
            if (board[i][y] == "?"):
                board[i][y] = "X"
        if (colTents[y] == colCount[y]):
            for i in range(0, len(board)):
                if (board[i][y] == "?"):
                    board[i][y] = "."

"""
Primary function to start the solving process. Runs the pre-move
strategies, then calls the recursive solver.
"""
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

"""
Recursive solver function. Checks for an empty
spot, then attempts to put a tent there. Runs the
other strategies, then recurse. If there are no
unknowns left, it checks to see if we've reached a goal
state; if we have, it returns true to signify the goal
has been reached.
"""
def solveRec(row, col):
    #print("------------------------")
    #printBoard()
    metadata = saveMetadata()
    if(isValid(row,col)):
        board[row][col] = "X"
        colCount[col] += 1
        rowCount[row] += 1
        markTentAdjGrass(row, col)
        markTentRowCol(row,col)
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

"""
In all but name, my main function. Starts everything.
"""
init()
if(solve()):
    print("Found a solution: ")
    printBoard()
else:
    print("Sorry, no solution could be found")
