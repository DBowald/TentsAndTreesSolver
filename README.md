For my project, I chose to do tents and trees. Here's my decision process for why I
decided to do tents and trees in boring old python:
1) Attempt to do Nurikabe in Matlab
2) Make slow progress
3) Realize finishing this will take more time than I have to spend on this
4) Panic
5) Do tents and trees in Python

Regardless, I'm pretty happy with the result.

Running the program:
The program can be run using the command line:
python solver.py <filename>

File Input:
Takes in a file, where the file has the following syntax:
Size
<n>x<m>
Rows
1
0
2
// Each row number on its own line
// E.g. the 1 would be index 0
Columns
2
1
1
// Same as rows
Trees
0,0
3,4
// Coordinates of trees in <row,column> format

Output:
Tells you whether a solution can be found. If it can,
it also includes an ascii art graphic of the solution.

Project representation:
2D list for board
Hashmaps for row and column numbers
Also hashmaps to keep track of tents

Strategies:
My program uses 5 constraint based strategies.
Two are done at the start:
1) Mark any spot not adjacent to a tree as grass
2) Check the rows and column numbers.
    2a) Checks for 0s, and fills in grass
    2b) Checks for areas where unknowns = row/col number,
        then fill in tents if they are equal.

Three are done after a tent is placed:
1) Mark all "tent adjacent" (including diagonals) spots
 as grass
2) Similar to 2b), but only for that row and column
3) Check if the number of tents in a row or column equals the row or
column number, and if it does, fill in the rest of the row or column
with grass.

If none of these work, it branches by polling for an unknown, saving
the board state, then marking that spot as an X.


