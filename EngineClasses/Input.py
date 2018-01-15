import pygame, sys
from pygame.locals import *

class Input:
    def __init__(self):
        self.pressedKeys = []
        self.unpressedKeys = []
        self.mousePressed = False
        self.mouseUnpressed = False
        self.resizable = False
        self.screen_size = (0, 0)
        self.mousePos = (0, 0)
        self.hoveredCell = (0, 0)
        self.lastCell = (0, 0)
        self.events = []

    def get(self):
        self.mouseUnpressed = False
        self.resizable = False
        self.unpressedKeys = []
        self.lastCell = self.hoveredCell

        self.events = pygame.event.get()
        for event in self.events:
            if event.type == QUIT:
                self.terminate()
            elif event.type == RESIZABLE:
                self.resizable = True
                self.screen_size = event.size
            elif event.type == KEYDOWN:
                self.pressedKeys.append(event.key)
            elif event.type == KEYUP:
                for key in self.pressedKeys:
                    if event.key == key:
                        self.pressedKeys.remove(key)
                    self.unpressedKeys.append(key)
            elif event.type == MOUSEMOTION:
                self.mousePos = event.pos
            elif event.type == MOUSEBUTTONDOWN:
                self.mousePressed = event.button
                self.mouseUnpressed = False
            elif event.type == MOUSEBUTTONUP:
                self.mousePressed = False
                self.mouseUnpressed = event.button

        self.checkForQuit()
        # if pygame.locals.K_ESCAPE in self.unpressedKeys:
        #     self.showConfirmExitAlert()

        # if my.gameRunning:
        #     self.hoveredPixel = my.map.screenToGamePix(self.mousePos)
        #     hoveredCoords = my.map.screenToCellCoords(self.mousePos)
        #     if not my.UIhover and my.map.inBounds(hoveredCoords):
        #         self.hoveredCell = my.map.screenToCellCoords(self.mousePos)
        #         self.hoveredCellType = my.map.cellType(self.hoveredCell)
        #     else:
        #         self.hoveredCell = None
        #         self.hoveredCellType = None

    def checkForQuit(self):
        """Terminate if QUIT events"""
        if K_ESCAPE in self.unpressedKeys:
            self.terminate()  # terminate if any QUIT events are present

    # def showConfirmExitAlert(self):
    #     """Shows a pop up alert asking the user if they want to quit, and pauses the program while doing so"""
    #     alertIsOpen = True
    #     alert = ui.ExitAlert()
    #     while alertIsOpen:
    #         alertIsOpen = alert.update()
    #         self.get()  # get input
    #         pygame.display.update()

    def terminate(self):
        """Safely end the program"""
        pygame.quit()
        sys.exit()
