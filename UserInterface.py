import pygame
import time
from copy import deepcopy
from SudokuSolver import SudokuSolver
from DoublyLinkedList import doublyLinkedList as DLL

class UserInterface():
    def __init__(self, window, BG_COLOR, windowDisplayed = "Main Menu"):
        self.window = window
        self.BG_COLOR = BG_COLOR
        self.windowDisplayed = windowDisplayed
        self.highlight = 0
        self.tempSS = SudokuSolver()

    #Draws Main Menu screen
    def mainMenu(self):
        (WINDOW_X, WINDOW_Y) = self.window.get_size()
        self.window.fill(self.BG_COLOR)

        mouse = pygame.mouse.get_pos()

        font = pygame.font.SysFont('arial', 70, bold=True)
        text = font.render("Sudoku", True, (0,114,227), self.BG_COLOR)
        textRect = text.get_rect()
        textRect.center = (450,250)

        (buttonWidth, buttonHeight) = (200,100)
        (buttonX, buttonY) = (WINDOW_X/2 - buttonWidth/2, WINDOW_Y/2 - buttonHeight/2 - 100)
        buttonCol = (115,165,200)
        buttonCol2 = (100,140,165)
        buttonFont = pygame.font.SysFont('arial', 50)
        buttonTxt = buttonFont.render('Start' , True , (0,0,0))

        if buttonX <= mouse[0] <= buttonX + buttonWidth and buttonY <= mouse[1] <= buttonY + buttonHeight:
            pygame.draw.rect(self.window, buttonCol2, [buttonX, buttonY, buttonWidth, buttonHeight])
        else:
            pygame.draw.rect(self.window, buttonCol, [buttonX, buttonY, buttonWidth, buttonHeight])
        self.window.blit(buttonTxt, (buttonX+buttonWidth/2 - 50, buttonY+buttonHeight/2 - 25))
        self.window.blit(text, textRect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.windowDisplayed = "Quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if buttonX <= mouse[0] <= buttonX + buttonWidth and buttonY <= mouse[1] <= buttonY + buttonHeight:
                    self.windowDisplayed = "Input Window"

        pygame.display.flip()

    #Displays the sudoku input window
    def inputWindow(self, ss):
        mouse = pygame.mouse.get_pos()
        #print(f"x: {mouse[0]} y: {mouse[1]}")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.windowDisplayed = "Quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                j = mouse[0]//100
                i = mouse[1]//100
                
                temp = deepcopy(self.tempSS.current.board)
                num = int((mouse[0]%100)//(100/3) + 3*((mouse[1]%100)//(100/3)) + 1)
                if num in temp[i][j]:
                    temp[i][j] = [num]
                    self.tempSS.DLL.delAfterCurrent(self.tempSS.current)
                    self.tempSS.DLL.insertToEnd(temp)
                    self.tempSS.current = self.tempSS.current.next
                    self.tempSS.soloTest()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if self.tempSS.current.prev is not None:
                        self.tempSS.current = self.tempSS.current.prev.prev
                if event.key == pygame.K_RIGHT:
                    if self.tempSS.current.next is not None:
                        self.tempSS.current = self.tempSS.current.next.next
                if event.key == pygame.K_SPACE:
                    self.tempSS.current.prev = None
                    ss.__init__(self.tempSS.current.board)
                    ss.solve()
                    ss.DLL.printLinkedList()
                    self.windowDisplayed = "Solution Window"


        self.window.fill(self.BG_COLOR)

        font = pygame.font.SysFont('arial', 90)
        smallfont = pygame.font.SysFont('arial', 30)

        for i in range(9):
            for j in range(9):
                textColor = (0,0,0)

                if len(self.tempSS.current.board[i][j]) == 1:
                    text = self.tempSS.current.board[i][j][0]
                    num = font.render(str(text),True,textColor,self.BG_COLOR)
                    numRect = num.get_rect()
                    numRect.center = (50+100*j,50+100*i)
                    self.window.blit(num, numRect)
                else:
                    for item in self.tempSS.current.board[i][j]:
                        for k in range(1,10):
                            if item == k:
                                text = k
                                break
                            else:
                                text = ""
                        note = smallfont.render(str(text),True,(100,100,100),self.BG_COLOR)
                        noteRect = note.get_rect()
                        noteRect.center = (100*j + 33*((k-1)%3) + 33/2, 100*i + 33*((k-1)//3) + 33/2)
                        self.window.blit(note, noteRect)

        for i in range(8):
            for j in range(2):
                if i == 2 or i == 5:
                    width = 3
                else:
                    width = 1

                if j == 0:
                    pygame.draw.line(self.window, (0,0,0),(100+100*i,0),(100+100*i,900),width)
                else:
                    pygame.draw.line(self.window, (0,0,0),(0,100+100*i),(900,100+100*i),width)
        
        pygame.display.flip()

    #Displays the solution
    def solutionWindow(self, ss):
        newHighlight = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.windowDisplayed = "Quit"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if ss.current.prev is not None:
                        ss.current = ss.current.prev
                        print(f"Board Count: {ss.current.count}")
                if event.key == pygame.K_RIGHT:
                    if ss.current.next is not None:
                        ss.current = ss.current.next
                        print(f"Board Count: {ss.current.count}")

                if event.key == pygame.K_1:
                    newHighlight = 1
                elif event.key == pygame.K_2:
                    newHighlight = 2
                elif event.key == pygame.K_3:
                    newHighlight = 3
                elif event.key == pygame.K_4:
                    newHighlight = 4
                elif event.key == pygame.K_5:
                    newHighlight = 5
                elif event.key == pygame.K_6:
                    newHighlight = 6
                elif event.key == pygame.K_7:
                    newHighlight = 7
                elif event.key == pygame.K_8:
                    newHighlight = 8
                elif event.key == pygame.K_9:
                    newHighlight = 9

                if newHighlight == self.highlight:
                    self.highlight = 0
                else:
                    self.highlight = newHighlight

        self.window.fill(self.BG_COLOR)

        font = pygame.font.SysFont('arial', 90)
        smallfont = pygame.font.SysFont('arial', 30)

        for i in range(9):
            for j in range(9):
                if len(ss.DLL.startNode.board[i][j]) == 1:
                    textColor = (0,0,0)
                else:
                    textColor = (0,114,227)

                if len(ss.current.board[i][j]) == 1:
                    text = ss.current.board[i][j][0]

                    if text == self.highlight:
                        textColor = (255,0,0)

                    num = font.render(str(text),True,textColor,self.BG_COLOR)
                    numRect = num.get_rect()
                    numRect.center = (50+100*j,50+100*i)
                    self.window.blit(num, numRect)
                else:
                    for item in ss.current.board[i][j]:
                        for k in range(1,10):
                            if item == k:
                                text = k
                                break
                            else:
                                text = ""
                        textColor = (100,100,100)
                        if text == self.highlight:
                            textColor = (0,0,255)

                        note = smallfont.render(str(text),True,textColor,self.BG_COLOR)
                        noteRect = note.get_rect()
                        noteRect.center = (100*j + 33*((k-1)%3) + 33/2, 100*i + 33*((k-1)//3) + 33/2)
                        self.window.blit(note, noteRect)

        for i in range(8):
            for j in range(2):
                if i == 2 or i == 5:
                    width = 3
                else:
                    width = 1

                if j == 0:
                    pygame.draw.line(self.window, (0,0,0),(100+100*i,0),(100+100*i,900),width)
                else:
                    pygame.draw.line(self.window, (0,0,0),(0,100+100*i),(900,100+100*i),width)
        
        pygame.display.flip()