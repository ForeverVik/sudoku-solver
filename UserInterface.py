import pygame
import time

class UserInterface():
    def __init__(self, window, BG_COLOR, windowDisplayed = "Main Menu"):
        self.window = window
        self.BG_COLOR = BG_COLOR
        self.windowDisplayed = windowDisplayed

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

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.windowDisplayed = "Quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if buttonX <= mouse[0] <= buttonX + buttonWidth and buttonY <= mouse[1] <= buttonY + buttonHeight:
                    self.windowDisplayed = "Solved Window"

        if buttonX <= mouse[0] <= buttonX + buttonWidth and buttonY <= mouse[1] <= buttonY + buttonHeight:
            pygame.draw.rect(self.window, buttonCol2, [buttonX, buttonY, buttonWidth, buttonHeight])
        else:
            pygame.draw.rect(self.window, buttonCol, [buttonX, buttonY, buttonWidth, buttonHeight])
        self.window.blit(buttonTxt, (buttonX+buttonWidth/2 - 50, buttonY+buttonHeight/2 - 25))
        self.window.blit(text, textRect)

        pygame.display.flip()

    #Displays the solution
    def solvedWindow(self, ss):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.windowDisplayed = "Quit"

        self.window.fill(self.BG_COLOR)

        font = pygame.font.SysFont('arial', 90)
        smallfont = pygame.font.SysFont('arial', 30)

        for i in range(9):
            for j in range(9):
                if len(ss.baseBoard[i][j]) == 1:
                    textColor = (0,0,0)
                else:
                    textColor = (0,114,227)

                if len(ss.currentBoard[i][j]) == 1:
                    text = ss.currentBoard[i][j][0]
                    num = font.render(str(text),True,textColor,self.BG_COLOR)
                    numRect = num.get_rect()
                    numRect.center = (50+100*j,50+100*i)
                    self.window.blit(num, numRect)
                else:
                    for item in ss.currentBoard[i][j]:
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