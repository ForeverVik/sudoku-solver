from copy import deepcopy
from DoublyLinkedList import doublyLinkedList as DLL

class SudokuSolver():
    def __init__(self, initialBoard=[[0,0,0,0,0,0,0,0,0],
                                  [0,0,0,0,0,0,0,0,0],
                                  [0,0,0,0,0,0,0,0,0],
                                  [0,0,0,0,0,0,0,0,0],
                                  [0,0,0,0,0,0,0,0,0],
                                  [0,0,0,0,0,0,0,0,0],
                                  [0,0,0,0,0,0,0,0,0],
                                  [0,0,0,0,0,0,0,0,0],
                                  [0,0,0,0,0,0,0,0,0]]):
        
        self.DLL = DLL()
        self.DLL.insertToEnd(initialBoard)
        self.current = self.DLL.startNode

        #Mark-up the given Sudoku board by filling in every empty square with every number 1-9
        for lineNum, line in enumerate(self.current.board):
            for num in range(len(line)):
                if line[num] == 0:
                    line[num] = [1,2,3,4,5,6,7,8,9]
                    self.current.board[lineNum] = line
                elif type(line[num]) == int:
                    line[num] = [line[num]]

        self.size = len(self.current.board)
        self.isSolved = False
        self.iterations = 0
        self.temp = []
        self.pairs = {}

    #Prints out the current board neatly
    def __str__(self):
        for i in self.current.board:
            for j in i:
                if len(j) > 1:
                    out = '.'
                else:
                    out = j[0]
                print(f"{out} ", end="")
            print()
        return ""

    #Prints out the initial board neatly
    def printInitial(self):
        for i in self.DLL.startNode.board:
            for j in i:
                if j == 0:
                    out = '.'
                else:
                    out = j
                print(f"{out} ", end="")
            print()
        return ""

    #Returns all possible numbers for the i,j square
    def getNumsAt(self, i, j):
        return self.current.board[i][j]
    
    def getSizeAt(self, i, j):
        return len(self.getNumsAt(i,j))
    
    def getGridAt(self, i, j):
        return 3*(i//3) + j//3
        
    def checkIfSolved(self):
        #If the board has not changed since the last time checkIfSolved() was called, return True
        #Or if every square has only one number, return True
        if self.temp == self.current.board:
            self.solved = True
            return True
    
        self.temp = deepcopy(self.current.board)
        for i in self.current.board:
            for j in i:
                if len(j) != 1:
                    self.solved = False
                    return False
        self.solved = True
        return True

    #Searches row (row) for squares that contain all numbers in num[], and returns their indicies
    #Acceptable row range: [0,8]
    #Acceptable num range: [1,9]
    def searchRow(self, row, num):
        if row < 0 or row > 8:
            raise ValueError
        for i in num:
            if i < 1 or i > 9:
                raise ValueError
        
        out = []
        for i in range(len(self.current.board[row])):
            if all(ele in self.current.board[row][i] for ele in num):
                out.append(i)
        return out

    #Searches column (col) for number (num) and returns all indecies that contain num
    def searchCol(self, col, num):
        if col < 0 or col > 8:
            raise ValueError
        for i in num:
            if i < 1 or i > 9:
                raise ValueError
        
        out = []
        for lineNum, line in enumerate(self.current.board):
            if all(ele in line[col] for ele in num):
                out.append(lineNum)
        return out
    
    #Searches the 3x3 grid that contains the square at row (row) and column (col) for number (num)
    #If onlyNum is False (default), returns all row-column pairs that contain [num]
    #If onlyNum is True, return all row-column pairs that contain ONLY [num]
    def searchGrid(self, row, col, num, onlyNum = False):
        if row < 0 or row > 8 or col < 0 or col > 8:
            raise ValueError
        for i in num:
            if i < 1 or i > 9:
                raise ValueError
        
        out = []
        if row < 3:
            if col < 3:
                rowRange = range(0,3)
                colRange = range(0,3)
            elif col < 6:
                rowRange = range(0,3)
                colRange = range(3,6)
            else:
                rowRange = range(0,3)
                colRange = range(6,9)
        elif row < 6:
            if col < 3:
                rowRange = range(3,6)
                colRange = range(0,3)
            elif col < 6:
                rowRange = range(3,6)
                colRange = range(3,6)
            else:
                rowRange = range(3,6)
                colRange = range(6,9)
        else:
            if col < 3:
                rowRange = range(6,9)
                colRange = range(0,3)
            elif col < 6:
                rowRange = range(6,9)
                colRange = range(3,6)
            else:
                rowRange = range(6,9)
                colRange = range(6,9)
           
        for i in rowRange:
            for j in colRange:
                if onlyNum == True:
                    if self.current.board[i][j] == num:
                        out.append([i,j])
                else:
                    if all(ele in self.current.board[i][j] for ele in num):
                        out.append([i,j])
        return out
    
    #Search through all the squares until a square n is found such that n has only one number in it
    #Remove the number from every square in the same row, column, and 3x3 as n
    def soloTest(self):
        _board = deepcopy(self.current.board)

        #Loop throught every square
        for i in range(self.size):
            for j in range(self.size):
                #If there is only one number in the current square
                if self.getSizeAt(i,j) == 1:
                    num = self.getNumsAt(i,j)[0]

                    for k in self.pairs:
                        for l in self.pairs[k]:
                            if num in l:
                                self.pairs[k].remove(l)

                    #Remove the number from every other square in the row
                    rowRemove = self.searchRow(i, [num])
                    rowRemove.remove(j)
                    for col in rowRemove:
                        if len(_board[i][col]) > 1 and _board[i][col].count(num):
                            _board[i][col].remove(num)
                    
                    #Remove the number from every other square in the column
                    colRemove = self.searchCol(j, [num])
                    colRemove.remove(i)
                    for row in colRemove:
                        if len(_board[row][j]) > 1 and _board[row][j].count(num):
                            _board[row][j].remove(num)
                    
                    #Remove the number from every other square in the 3x3 grid
                    gridRemove = self.searchGrid(i, j, [num])
                    gridRemove.remove([i,j])
                    for grid in gridRemove:
                        if len(_board[grid[0]][grid[1]]) > 1 and _board[grid[0]][grid[1]].count(num):
                            _board[grid[0]][grid[1]].remove(num)
        
        self.DLL.insertToEnd(_board, "solo")
        self.current = self.current.next
    
    #Find any squares that contain a number n that shows up only once in it's row, column, or grid, and removes n from any squares in it's row, column, and grid
    def singlesTest(self):
        _board = deepcopy(self.current.board)
            
        for i in range(self.size):
            for j in range(self.size):
            
                for num in _board[i][j]:
                    if num in _board[i][j]:
                        rowOccurences = self.searchRow(i, [num])
                        rowOccurences.remove(j)
                        colOccurences = self.searchCol(j, [num])
                        colOccurences.remove(i)
                        gridOccurences = self.searchGrid(i, j, [num])
                        gridOccurences.remove([i,j])

                        if len(rowOccurences) == 0 or len(colOccurences) == 0 or len(gridOccurences) == 0:
                            for k in rowOccurences:
                                if _board[i][k].count(num) and len(_board[i][k]) > 1:
                                    _board[i][k].remove(num)
                            
                            for k in colOccurences:
                                if _board[k][j].count(num) and len(_board[k][j]) > 1:
                                    _board[k][j].remove(num)
                            
                            for k in gridOccurences:
                                if _board[k[0]][k[1]].count(num) and len(_board[k[0]][k[1]]) > 1:
                                    _board[k[0]][k[1]].remove(num)

                            _board[i][j] = [num]

        self.DLL.insertToEnd(_board, "singles")
        self.current = self.current.next
                            
    def lineTest(self):
        _board = deepcopy(self.current.board)
            
        for i in range(self.size):
            for j in range(self.size):
                for num in _board[i][j]:
                    sameRow = True
                    sameCol = True
                    nums = self.searchGrid(i, j, [num])
                    nums.remove([i,j])
                    for k in nums:
                        if k[0] != i:
                            sameRow = False
                        if k[1] != j:
                            sameCol = False
                        
                    if sameRow:
                        rowRemove = self.searchRow(i, [num])
                        if len(rowRemove) > 2:
                            for col in rowRemove:
                                if self.getGridAt(i,j) != self.getGridAt(i,col):
                                    if len(_board[i][col]) > 1 and _board[i][col].count(num):
                                        _board[i][col].remove(num)
                    
                    if sameCol:
                        colRemove = self.searchCol(j, [num])
                        if len(colRemove) > 2:
                            for row in colRemove:
                                if self.getGridAt(i,j) != self.getGridAt(row,j):
                                    if len(_board[row][j]) > 1 and _board[row][j].count(num):
                                        _board[row][j].remove(num)
        
        self.DLL.insertToEnd(_board, "line")
        self.current = self.current.next

    #Finds any squares in a grid that only contain some pair of numbers (a,b). These squares can only contain a or b
    #Therefore, remove any occurences of a and b from the other squares in the grid
    #And if the two squares are in the same row, remove any occurences of a and b from the other squares in the row
    #And if the two squares are in the same column, remove any occurences of and b from the other squares in the row 
    def pairTest(self):
        _board = deepcopy(self.current.board)

        for i in range(self.size):
            for j in range(self.size):
                toRemove = []
                if len(_board[i][j]) == 2:
                    nums = self.getNumsAt(i,j)
                    
                    identicalGrid = self.searchGrid(i, j, _board[i][j], True)
                    if len(identicalGrid) == 2:
                        for n in nums:
                            sameGrid = self.searchGrid(i, j, [n])
                            for g in identicalGrid:
                                sameGrid.remove(g)
                            
                            for g in sameGrid:
                                toRemove.append([g[0],g[1],n])
                        
                        if identicalGrid[0][0] == identicalGrid[1][0]:
                            for n in nums:
                                sameRow = self.searchRow(i, [n])
                                for g in identicalGrid:
                                    sameRow.remove(g[1])
                                
                                for g in sameRow:
                                    toRemove.append([i,g,n])
                        
                        if identicalGrid[0][1] == identicalGrid[1][1]:
                            for n in nums:
                                sameCol = self.searchCol(j, [n])
                                for g in identicalGrid:
                                    sameCol.remove(g[0])
                                
                                for g in sameCol:
                                    toRemove.append([g,j,n])

                for t in toRemove:
                        if len(_board[t[0]][t[1]]) > 1 and _board[t[0]][t[1]].count(t[2]):
                            _board[t[0]][t[1]].remove(t[2])     

        self.DLL.insertToEnd(_board, "pair")
        self.current = self.current.next                                    
                                                                   
    #If any grid contains exactly two squares with some pair of numbers (a,b), and neither a nor b occur anywhere else in the grid
    #Those squares can only contain a or b. Remove any excess numbers from those squares.
    def hiddenPairTest(self):
        _board = deepcopy(self.current.board)

        for i in range(self.size):
            for j in range(self.size):
                if len(_board[i][j]) > 1:
                    toRemove = []
                    for k in range(len(_board[i][j])):
                        for l in range(k+1, len(_board[i][j])):
                            a = _board[i][j][k]
                            b = _board[i][j][l]

                            gridPairs = self.searchGrid(i, j, [a,b])

                            if len(gridPairs) == 2 and len(self.searchGrid(i,j,[a])) == 2 and len(self.searchGrid(i,j,[b])) == 2:
                                #Remove all excess numbers in the square
                                temp = deepcopy(_board[i][j])
                                temp.remove(a)
                                temp.remove(b)

                                for g in gridPairs:
                                    for m in temp:
                                        toRemove.append([g[0], g[1], m])
                                
                                #Used for XY Wing Test
                                if f"{a}{b}" in self.pairs:
                                    self.pairs[f"{a}{b}"].append((i,j))
                                else:
                                    self.pairs[f"{a}{b}"] = [(i,j)]
                    
                    for t in toRemove:
                        if len(_board[t[0]][t[1]]) > 1 and _board[t[0]][t[1]].count(t[2]):
                            _board[t[0]][t[1]].remove(t[2])
        
        self.DLL.insertToEnd(_board, "hidden pair")
        self.current = self.current.next

    #HIDDEN TRIPLE TEST

    #Recursively applies solving algorithms to the board until solved
    def solve(self):
        self.iterations+=1

        self.soloTest()
        self.singlesTest()
        self.lineTest()
        self.hiddenPairTest()
        self.pairTest()

        if self.checkIfSolved():
                print(self.pairs)
                return
        self.solve()