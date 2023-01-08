'''
The statemanager is used by gui.py to determine which state the game is in 
to manage correct buttons available to be selected.
'''

class State:

    #4 possible states
    #State 1: Main Menu
    #State 2: Hall of Fame, includes Main Menu display
    #State 3: Player Name Entry
    #State 4: In Game

    #States are used to ensure non-visible buttons cannot be clicked
    #This is as the way buttons are pressed is by findigng the location and finding a button
    #surrounding it.
    def __init__(self) -> None:
        self.mainMenu = 1
        self.HOF = 2
        self.NameEntry = 3
        self.Game = 4
        self.currentState = self.setMainMenu()

    def getState(self):
        return self.currentState

    def setMainMenu(self):
        self.currentState = self.mainMenu

    def setHOF(self):
        self.currentState = self.HOF

    def setNameEntry(self):
        self.currentState = self.NameEntry
    
    def setGame(self):
        self.currentState = self.Game

    