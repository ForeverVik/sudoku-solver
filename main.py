import pygame
import json
from UserInterface import UserInterface
from SudokuSolver import SudokuSolver
import time

def main():
    #Pygame Initialization
    pygame.init()
    with open('settings.json') as s:
        settings = json.load(s)
    window = pygame.display.set_mode([settings["window"]["WIDTH"], settings["window"]["HEIGHT"]])
    pygame.display.set_caption("Sudoku Solver")
    pygame.display.set_icon(pygame.image.load("assets/icon.png"))
    UI = UserInterface(window, settings["window"]["BG_COLOR"])

    #Gets the sudoku board from the json file
    with open('sudoku.json') as f:
        req = json.load(f)
    baseBoard = req['newboard']['grids'][0]['value']

    ss = SudokuSolver(baseBoard)
    st = time.time()

    #Recursively applies solving algorithms to the board until solved
    ss.solve()
    count = ss.iterations
    et = time.time()
    print(f"Board solved in {count} iterations, {et-st} seconds")
    
    #Displays windows based on the UI.windowDisplayed variable
    while UI.windowDisplayed != "Quit":
        if UI.windowDisplayed == "Main Menu":
            UI.mainMenu()
        elif UI.windowDisplayed == "Solved Window":
            UI.solvedWindow(ss)

    pygame.quit()


if __name__ == '__main__':
    main()