from copy import deepcopy

class SudokuSolver():
    def __init__(self, baseBoard):
        self.baseSudoku = deepcopy(baseBoard)

        #Mark-up the given Sudoku board by filling in every empty square with every number 1-9
        for lineNum, line in enumerate(baseBoard):
            for num in range(len(line)):
                if line[num] == 0:
                    line[num] = [1,2,3,4,5,6,7,8,9]
                    baseBoard[lineNum] = line
                else:
                    line[num] = [line[num]]

        self.baseBoard = deepcopy(baseBoard)
        self.prevBoard = deepcopy(baseBoard)
        self.currentBoard = deepcopy(baseBoard)
        self.size = len(self.baseBoard)
        self.isSolved = False
        self.iterations = 0
        self.temp = []

    #Prints out the current board neatly
    def __str__(self):
        for i in self.currentBoard:
            for j in i:
                if len(j) > 1:
                    out = '.'
                else:
                    out = j[0]
                print(f"{out} ", end="")
            print()
        return ""

    #Prints out the base board neatly
    def printBase(self):
        for i in self.baseSudoku:
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
        return self.currentBoard[i][j]
    
    def getSizeAt(self, i, j):
        return len(self.getNumsAt(i,j))
    
    def getGridAt(self, i, j):
        return i//3 + j//3
        
    def checkIfSolved(self):
        #If the board has not changed since the last time checkIfSolved() was called, return True
        #Or if every square has only one number, return True
        if self.temp == self.currentBoard:
            self.solved = True
            return True
    
        self.temp = deepcopy(self.currentBoard)
        for i in self.currentBoard:
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
        for i in range(len(self.currentBoard[row])):
            if all(ele in self.currentBoard[row][i] for ele in num):
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
        for lineNum, line in enumerate(self.currentBoard):
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
                    if self.currentBoard[i][j] == num:
                        out.append([i,j])
                else:
                    if all(ele in self.currentBoard[i][j] for ele in num):
                        out.append([i,j])
        return out
    
    #Search through all the squares until a square n is found such that n has only one number in it
    #Remove the number from every square in the same row, column, and 3x3 as n
    def soloTest(self):
        self.prevBoard = deepcopy(self.currentBoard)

        #Loop throught every square
        for i in range(self.size):
            for j in range(self.size):
                #If there is only one number in the current square
                if self.getSizeAt(i,j) == 1:
                    num = self.getNumsAt(i,j)[0]

                    #Remove the number from every other square in the row
                    rowRemove = self.searchRow(i, [num])
                    rowRemove.remove(j)
                    for col in rowRemove:
                        if len(self.currentBoard[i][col]) > 1 and self.currentBoard[i][col].count(num):
                            self.currentBoard[i][col].remove(num)
                    
                    #Remove the number from every other square in the column
                    colRemove = self.searchCol(j, [num])
                    colRemove.remove(i)
                    for row in colRemove:
                        if len(self.currentBoard[row][j]) > 1 and self.currentBoard[row][j].count(num):
                            self.currentBoard[row][j].remove(num)
                    
                    #Remove the number from every other square in the 3x3 grid
                    gridRemove = self.searchGrid(i, j, [num])
                    gridRemove.remove([i,j])
                    for grid in gridRemove:
                        if len(self.currentBoard[grid[0]][grid[1]]) > 1 and self.currentBoard[grid[0]][grid[1]].count(num):
                            self.currentBoard[grid[0]][grid[1]].remove(num)
    
    #Find any squares that contain a number n that shows up only once in it's row, column, or grid, and removes n from any squares in it's row, column, and grid
    def singlesTest(self):
        self.prevBoard = deepcopy(self.currentBoard)
            
        for i in range(self.size):
            for j in range(self.size):
            
                for num in self.currentBoard[i][j]:
                    if num in self.currentBoard[i][j]:
                        rowOccurences = self.searchRow(i, [num])
                        rowOccurences.remove(j)
                        colOccurences = self.searchCol(j, [num])
                        colOccurences.remove(i)
                        gridOccurences = self.searchGrid(i, j, [num])
                        gridOccurences.remove([i,j])

                        if len(rowOccurences) == 0 or len(colOccurences) == 0 or len(gridOccurences) == 0:
                            for k in rowOccurences:
                                if self.currentBoard[i][k].count(num) and len(self.currentBoard[i][k]) > 1:
                                    self.currentBoard[i][k].remove(num)
                            
                            for k in colOccurences:
                                if self.currentBoard[k][j].count(num) and len(self.currentBoard[k][j]) > 1:
                                    self.currentBoard[k][j].remove(num)
                            
                            for k in gridOccurences:
                                if self.currentBoard[k[0]][k[1]].count(num) and len(self.currentBoard[k[0]][k[1]]) > 1:
                                    self.currentBoard[k[0]][k[1]].remove(num)

                            self.currentBoard[i][j] = [num]
                            
    def lineTest(self):
        self.prevBoard = deepcopy(self.currentBoard)
            
        for i in range(self.size):
            for j in range(self.size):
                for num in self.currentBoard[i][j]:
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
                        for col in rowRemove:
                            if self.getGridAt(i,j) != self.getGridAt(i,col):
                                if len(self.currentBoard[i][col]) > 1 and self.currentBoard[i][col].count(num):
                                    self.currentBoard[i][col].remove(num)
                    
                    if sameCol:
                        colRemove = self.searchCol(j, [num])
                        for row in colRemove:
                            if self.getGridAt(i,j) != self.getGridAt(row,j):
                                if len(self.currentBoard[row][j]) > 1 and self.currentBoard[row][j].count(num):
                                    self.currentBoard[row][j].remove(num)

    #Finds any squares in a grid that only contain some pair of numbers (a,b). These squares can only contain a or b
    #Therefore, remove any occurences of a and b from the other squares in the grid
    #And if the two squares are in the same row, remove any occurences of a and b from the other squares in the row
    #And if the two squares are in the same column, remove any occurences of and b from the other squares in the row 
    def pairTest(self):
        self.prevBoard = deepcopy(self.currentBoard)

        for i in range(self.size):
            for j in range(self.size):
                toRemove = []
                if len(self.currentBoard[i][j]) == 2:
                    a = self.currentBoard[i][j][0]
                    b = self.currentBoard[i][j][1]

                    identicalGrid = self.searchGrid(i, j, self.currentBoard[i][j], True)
                    if len(identicalGrid) == 2:
                        sameGrid = self.searchGrid(i, j, [a])
                        for g in identicalGrid:
                            sameGrid.remove(g)
                        
                        for g in sameGrid:
                            toRemove.append([g[0],g[1],a])

                        sameGrid = self.searchGrid(i, j, [b])
                        for g in identicalGrid:
                            sameGrid.remove(g)
                        
                        for g in sameGrid:
                            toRemove.append([g[0],g[1],b])
                        
                        if identicalGrid[0][0] == identicalGrid[1][0]:
                            sameRow = self.searchRow(i, [a])
                            for g in identicalGrid:
                                sameRow.remove(g[1])
                            
                            for g in sameRow:
                                toRemove.append([g[0],g[1],a])
                            
                            sameRow = self.searchRow(i, [b])
                            for g in identicalGrid:
                                sameRow.remove(g[1])
                            
                            for g in sameRow:
                                toRemove.append([g[0],g[1],b])
                        
                        if identicalGrid[0][1] == identicalGrid[1][1]:
                            sameCol = self.searchCol(j, [a])
                            for g in identicalGrid:
                                sameCol.remove(g[0])
                            
                            for g in sameCol:
                                toRemove.append([g[0],g[1],a])
                            
                            sameCol = self.searchCol(j, [b])
                            for g in identicalGrid:
                                sameCol.remove(g[0])
                            
                            for g in sameCol:
                                toRemove.append([g[0],g[1],b])

                for t in toRemove:
                        if len(self.currentBoard[t[0]][t[1]]) > 1 and self.currentBoard[t[0]][t[1]].count(t[2]):
                            self.currentBoard[t[0]][t[1]].remove(t[2])                                         
                                                                   
    #If any grid contains exactly two squares with some pair of numbers (a,b), and neither a nor b occur anywhere else in the grid
    #Those squares can only contain a or b. Remove any excess numbers from those squares.
    def hiddenPairTest(self):
        self.prevBoard = deepcopy(self.currentBoard)

        for i in range(self.size):
            for j in range(self.size):
                if len(self.currentBoard[i][j]) > 1:
                    toRemove = []
                    for k in range(len(self.currentBoard[i][j])):
                        for l in range(k+1, len(self.currentBoard[i][j])):
                            a = self.currentBoard[i][j][k]
                            b = self.currentBoard[i][j][l]

                            gridPairs = self.searchGrid(i, j, [a,b])

                            if len(gridPairs) == 2 and len(self.searchGrid(i,j,[a])) == 2 and len(self.searchGrid(i,j,[b])) == 2:
                                #Remove all excess numbers in the square
                                temp = deepcopy(self.currentBoard[i][j])
                                temp.remove(a)
                                temp.remove(b)

                                for g in gridPairs:
                                    for m in temp:
                                        toRemove.append([g[0], g[1], m])
                    
                    for t in toRemove:
                        if len(self.currentBoard[t[0]][t[1]]) > 1 and self.currentBoard[t[0]][t[1]].count(t[2]):
                            self.currentBoard[t[0]][t[1]].remove(t[2])
                                

    ##Recursively applies solving algorithms to the board until solved
    def solve(self):
        self.iterations+=1
        self.soloTest()
        self.singlesTest()
        self.lineTest()
        self.hiddenPairTest()
        self.pairTest()

        if self.checkIfSolved():
                return
        self.solve()
            
        '''                                                       
    def pairTest(self):
        for i in range(self.size):
            for j in range(self.size):
                if len(self.currentBoard[i][j]) == 2:
                    a = self.currentBoard[i][j][0]
                    b = self.currentBoard[i][j][1]
                    sameRow = self.searchRow(i, [a,b])
                    sameRow.remove(j)
                    sameCol = self.searchCol(j, [a,b])
                    sameCol.remove(i)

                    for k in sameRow:
                        if self.getGridAt(i,j) == self.getGridAt(i,k) and self.currentBoard[i][k] == self.currentBoard[i][j]:
                            print(f"examining pair {a},{b} in row {i} col {j} and row {i} col {k}")
                            print(self)

                            gridRemoveA = self.searchGrid(i, j, [a])
                            gridRemoveA.remove([i,j])
                            gridRemoveA.remove([i,k])

                            gridRemoveB = self.searchGrid(i, j, [b])
                            gridRemoveB.remove([i,j])
                            gridRemoveB.remove([i,k])

                            for grid in gridRemoveB:
                                if len(self.currentBoard[grid[0]][grid[1]]) > 1 and self.currentBoard[grid[0]][grid[1]].count(a):
                                    self.currentBoard[grid[0]][grid[1]].remove(a)
                            for grid in gridRemoveB:
                                if len(self.currentBoard[grid[0]][grid[1]]) > 1 and self.currentBoard[grid[0]][grid[1]].count(b):
                                    self.currentBoard[grid[0]][grid[1]].remove(b)

                            rowRemoveA = self.searchRow(i, [a])
                            rowRemoveA.remove(j)
                            rowRemoveA.remove(k)

                            rowRemoveB = self.searchRow(i, [b])
                            rowRemoveB.remove(j)
                            rowRemoveB.remove(k)
        
                            for col in rowRemoveA:
                                if len(self.currentBoard[i][col]) > 1 and self.currentBoard[i][col].count(a):
                                    self.currentBoard[i][col].remove(a)
                            
                            for col in rowRemoveB:
                                if len(self.currentBoard[i][col]) > 1 and self.currentBoard[i][col].count(b):
                                    self.currentBoard[i][col].remove(b)

                    for k in sameCol:
                        if self.getGridAt(i,j) == self.getGridAt(k,j) and self.currentBoard[k][j] == self.currentBoard[i][j]:
                            print(self.currentBoard[k][j])
                            print(f"VERT examining pair {a},{b} in row {i} col {j} and row {k} col {j}")
                            print(self)

                            gridRemoveA = self.searchGrid(i, j, [a])
                            gridRemoveA.remove([i,j])
                            gridRemoveA.remove([k,j])

                            gridRemoveB = self.searchGrid(i, j, [b])
                            gridRemoveB.remove([i,j])
                            gridRemoveB.remove([k,j])

                            for grid in gridRemoveB:
                                if len(self.currentBoard[grid[0]][grid[1]]) > 1 and self.currentBoard[grid[0]][grid[1]].count(a):
                                    self.currentBoard[grid[0]][grid[1]].remove(a)
                            for grid in gridRemoveB:
                                if len(self.currentBoard[grid[0]][grid[1]]) > 1 and self.currentBoard[grid[0]][grid[1]].count(b):
                                    self.currentBoard[grid[0]][grid[1]].remove(b)

                            colRemoveA = self.searchCol(j, [a])
                            colRemoveA.remove(i)
                            colRemoveA.remove(k)

                            colRemoveB = self.searchCol(j, [b])
                            colRemoveB.remove(i)
                            colRemoveB.remove(k)
        
                            for row in colRemoveA:
                                if len(self.currentBoard[row][j]) > 1 and self.currentBoard[row][j].count(a):
                                    self.currentBoard[row][j].remove(a)
                            
                            for row in colRemoveB:
                                if len(self.currentBoard[row][j]) > 1 and self.currentBoard[row][j].count(b):
                                    self.currentBoard[row][j].remove(b)
    '''    