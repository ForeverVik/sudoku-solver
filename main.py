import pygame
import json
from UserInterface import UserInterface
from SudokuSolver import SudokuSolver

def main():
    #Pygame Initialization
    pygame.init()
    with open('settings.json') as s:
        settings = json.load(s)
    window = pygame.display.set_mode([settings["window"]["WIDTH"], settings["window"]["HEIGHT"]])
    pygame.display.set_caption("Sudoku Solver")
    pygame.display.set_icon(pygame.image.load("assets/icon.png"))

    #UI and SS Initialization
    UI = UserInterface(window, settings["window"]["BG_COLOR"])
    ss = SudokuSolver()

    #Displays windows based on the UI.windowDisplayed variable
    while UI.windowDisplayed != "Quit":
        match UI.windowDisplayed:
            case "Main Menu":
                UI.mainMenu()
            case "Input Window":
                UI.inputWindow(ss)
            case "Solution Window":
                UI.solutionWindow(ss)
            case _:
                print("unexpected window name")
                break

    pygame.quit()

if __name__ == '__main__':
    main()