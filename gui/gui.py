from graphics import *
from .keyboard import Keyboard
from .grid import Grid
from .gui_statemanager import State

class GUI:

    def __init__(self) -> None:
        self.window = GraphWin("PyWord", 700, 900)
        self.window.setBackground("white")

        #Dictionaries of each button to get the location of it for detecting which is clicked
        #For main menu
        self.buttonsMM = {}
        #For name entry
        self.buttonsNE = {}
        #For in game
        self.buttonsIG = {}

        #Create key objects
        self.keyboard = ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "A", "S", "D",
        "F", "G", "H", "J", "K", "L", "Enter", "Z", "X", "C", "V", "B", "N", "M", "Back"]
        self.keys = []
        self.keyboardIndex = 0
        #Setup key attributes
        self.__init_keys()

        #Create grid objects
        self.grid = []
        self.__init_grid()

        self.guess_Letters = [] #Stores current rows guessed letters prior to hitting enter
        self.all_guess_letters = [] #Stores all guess letters in current round
        self.guess_Grid = [] #Stores guess grid objects to be filled depending on guesses

        #State 1: Main Menu
        #State 2: Hall of Fame, includes Main Menu display
        #State 3: Player Name Entry
        #State 4: In Game
        self.state = State()
        
        self.hof_Objects = []
        self.menu_Objects = []
        self.name_Objects = []
    #Round drawing methods
    def draw_round(self):
        #Sets the game state
        self.state.setGame()
        #Draw the game
        self.draw_keyboard()
        self.draw_grid()

    def reset_round(self):
        self.__reset_grid()
        self.guess_Grid = []
        self.__reset_keyboard()

    def undraw(self, choice):

        if choice == "New Game":
            for obj in self.menu_Objects:
                obj.undraw()
            for obj in self.hof_Objects:
                obj.undraw()
        elif choice == "Hall of Fame":
            for obj in self.hof_Objects:
                obj.undraw()
        elif choice == "Enter":
            for obj in self.name_Objects:
                obj.undraw()
        elif choice == "Game":
            self.reset_round()
            self.undraw_keyboard()
            self.undraw_grid()

    def draw_game_text(self, text):
        display = Text(Point(350, 50), text)
        display.setSize(16)
        display.draw(self.window)
        self.wait_for_click()
        display.undraw()
        
    #Keyboard methods
    def __init_keys(self):
        #Set key letter
        for keyLetter in self.keyboard:
            key = Keyboard()
            key.letter = keyLetter
            self.keys.append(key)

        #Set key location
        self.keyboardIndex = 0

        #First row of keys
        x1, x2, y1, y2 = 50, 100, 650, 710
        for i in range(10):
            ul = Point(x1, y1)
            lr = Point(x2, y2)
            self.__init_keyObj(ul, lr)
            self.__init_letterObj(ul, lr)
            x1 += 60
            x2 += 60
            self.keyboardIndex += 1

        #Second Row
        x1, x2 = 80, 130
        y1 += 70
        y2 += 70
        for j in range(9):
            ul = Point(x1, y1)
            lr = Point(x2, y2)
            self.__init_keyObj(ul, lr)
            self.__init_letterObj(ul, lr)
            x1 += 60
            x2 += 60
            self.keyboardIndex += 1
        x1, x2 = 140, 190
        y1 += 70
        y2 += 70

        #Setup enter key location
        ul = Point(50, y1)
        lr = Point(130, y2)
        self.__init_keyObj(ul, lr)
        self.__init_letterObj(ul, lr)
        self.keyboardIndex += 1
        #Third row
        for j in range(7):
            ul = Point(x1, y1)
            lr = Point(x2, y2)
            self.__init_keyObj(ul, lr)
            self.__init_letterObj(ul, lr)
            x1 += 60
            x2 += 60
            self.keyboardIndex += 1
        #And backspace key
        ul = Point(x1, y1)
        lr = Point(640, y2)
        self.__init_keyObj(ul, lr)
        self.__init_letterObj(ul, lr)
        
    def __init_keyObj(self, ul, lr):
        #Set each keys boundry
        self.keys[self.keyboardIndex].ul = ul
        self.keys[self.keyboardIndex].lr = lr
        #Create actual key graphic object, not drawn yet
        self.keys[self.keyboardIndex].keyObj = Rectangle(ul, lr)
        #Add to buttons that can be clicked
        self.buttonsIG[self.keyboard[self.keyboardIndex]] = [ul, lr]

    def __init_letterObj(self, ul, lr):
        #Get center of key to create text at
        centerX = lr.getX() - ((lr.getX() - ul.getX()) / 2)
        centerY = ul.getY() - ((ul.getY() - lr.getY()) / 2)
        #Creates the letter object, at the point with the keys .letter text, stores object in this keys .letterObj attribute
        self.keys[self.keyboardIndex].letterObj = Text(Point(centerX, centerY), self.keys[self.keyboardIndex].letter)
        self.keys[self.keyboardIndex].letterObj.setSize(20) #Set the right size for the letter
    
    def draw_keyboard(self):
        for key in self.keys:
            key.keyObj.draw(self.window)
            key.letterObj.draw(self.window)

    def undraw_keyboard(self):
        for key in self.keys:
            key.keyObj.undraw()
            key.letterObj.undraw()

    def fill_key(self, letter, color):
        #the keyboard key list has all uppercase, so ensure letter is uppercase
        letter = letter.upper()
        #keys and keyboard(key letter list) has same indexing, so get key at index of the letter
        key = self.keys[self.keyboard.index(letter)]
        #If the key is not colored lime green, can change color. Don't want to change if it's already lime green
        if key.color != "lime green":
            key.keyObj.setFill(color)
            key.color = color
    
    def __reset_keyboard(self):
        #Called between rounds to clear coloring on keyboard
        for key in self.keys:
            key.keyObj.setFill("white")
            key.color = "white"

    #Grid Methods
    def __init_grid(self):
        rows = 6
        colums = 5
        for i in range(rows*colums):
            box = Grid()
            self.grid.append(box)
        gridIndex = 0
        y1, y2 = 100, 175
        for i in range(rows):
            #6 Rows
            x1, x2 = 142, 217
            for j in range(colums):
                #Setup cords for a single row
                ul = Point(x1, y1)
                lr = Point(x2, y2)
                self.__init_gridObj(ul, lr, gridIndex, i, j)
                gridIndex += 1
                x1 += 85
                x2 += 85
            #Move y to start next row
            y1 += 90
            y2 += 90

    def __init_gridObj(self, ul, lr, index, row, column):
        self.grid[index].gridObj = Rectangle(ul, lr)
        self.grid[index].gridObj.setWidth(2)
    
    def draw_grid(self):
        for box in self.grid:
            box.gridObj.draw(self.window)

    def undraw_grid(self):
        for box in self.grid:
            box.gridObj.undraw()
    
    def fill_grid_box(self, row, column, color):
        #Every 5 elements in list guess grid are a row
        #So, if higher than first row, multiply by 5 to get to beginning of next row,
        #Then add index to get the correct element to color
        index = ((row - 1) * 5) + column
        self.grid[index].gridObj.setFill(color)

    def __reset_grid(self):
        for box in self.grid:
            box.gridObj.setFill("white")
            self.undraw_guess_letter()
        for letter in self.all_guess_letters:
            letter.undraw()
    
    #Grid Letter Methods
    def draw_guess_letter(self, row, index, letter):
        #Center of first row first box:
        startBox = Point(180, 137)
        x = startBox.getX() + (index-1)*85 #Only want to add if more than 1
        y = startBox.getY() + (row-1)*90
        text = Text(Point(x, y), letter)
        text.setSize(20)
        text.draw(self.window)
        self.guess_Letters.append(text)
    

    def undraw_guess_letter(self):
        #Undraws the most recent letter guessed
        if len(self.guess_Letters) > 0:
            letter = self.guess_Letters.pop()
            letter.undraw()

    def clear_guess_letters(self):
        #Called everytime a valid guess is entered so no rows previous
        #to current one can be modified
        for letter in self.guess_Letters:
            self.all_guess_letters.append(letter)
        
        self.guess_Letters = []
        
    #Input Methods
    def wait_for_click(self):
        #waits for the mouse to click somepointin the window or for any
        #key to be pressed
        while True:
            clickPoint = self.window.checkMouse()
            if clickPoint is not None:
                return
            clickKey = self.window.checkKey()
            if clickKey != "":
                return
    
    def get_selection(self):
        #Gets a point selected by the mouse or a key entered
        while True:
            clickPoint = self.window.checkMouse()

            if clickPoint is not None:
                button = self.__find_clicked(clickPoint)
                if button is not None:
                    return button
            clickKey = ""
            clickKey = self.window.checkKey()
            if clickKey != "":
                if clickKey == "Return":
                    return "Enter"
                elif clickKey == "BackSpace":
                    return "Back"
                else:
                    return clickKey.upper()

    def __find_clicked(self, pointClicked):
        #Search dictionary to find which button was clicked

        buttonList = []
        pointList = []
        if (self.state.getState() == self.state.mainMenu):
            #Main menu
            buttonList = list(self.buttonsMM.keys())
            pointList = list(self.buttonsMM.values())
        elif (self.state.getState() == self.state.HOF):
            #Main menu/Hall of Fame
            buttonList = list(self.buttonsMM.keys())
            pointList = list(self.buttonsMM.values())
        elif (self.state.getState() == self.state.NameEntry):
            #Player name entry
            buttonList = list(self.buttonsNE.keys())
            pointList = list(self.buttonsNE.values())
        elif (self.state.getState() == self.state.Game):
            #In Game
            buttonList = list(self.buttonsIG.keys())
            pointList = list(self.buttonsIG.values())

        for value in pointList:
            #Get x and y of each of 2 points
            ul = value[0]
            lr = value[1]
            
            ulX = ul.getX()
            ulY = ul.getY()

            lrX = lr.getX()
            lrY = lr.getY()

            #If the point that is clicked is greater than the upper left x, and less than the lower right x, it is within the bounds of k's x value
            #If the point that is clicked is grater than the upper left y, and less than the lower right y, it is within the bounds of k's y value
            #If both, button k was clicked
            if ((pointClicked.getX() > ulX and pointClicked.getX() < lrX) and (pointClicked.getY() > ulY and pointClicked.getY() < lrY)):
                #Return the key(button) corresponding to current value 
                return buttonList[pointList.index(value)]

        #If never found the point clicked, don't do anything
            
    #Main Menu Methods
    def main_menu(self):
        self.state.setMainMenu()
        self.__draw_main_menu()
        return(self.get_selection())

    def __draw_main_menu(self) -> None:

        x1 = 100
        x2 = 600
        y1 = 100
        y2 = 200
        self.__draw_menu_button(x1, x2, y1, y2, "New Game")
        y1 += 125
        y2 += 125
        self.__draw_menu_button(x1, x2, y1, y2, "Hall of Fame")
        y1 += 125
        y2 += 125
        self.__draw_menu_button(x1, x2, y1, y2, "Quit")

    def __draw_menu_button(self, x1, x2, y1, y2, displayText):
        ul = Point(x1, y1)
        lr = Point(x2, y2)
        button = Rectangle(ul, lr)
        button.setWidth(5)
        button.draw(self.window)
        centerPointx = x2 - ((x2-x1)/2)
        centerPointy = y2 - ((y2-y1)/2)
        text = Text(Point(centerPointx, centerPointy), displayText)
        text.setSize(32)
        text.draw(self.window)
        self.buttonsMM[displayText] = [ul, lr]

        #Add objects to list so they can be undrawn later
        self.menu_Objects.append(button)
        self.menu_Objects.append(text)

    #Hall of Fame Methods
    def draw_HOF(self, hof):
        title = Text(Point(350, 500), "Hall of Fame")
        title.setSize(22)
        title.draw(self.window)
        titleKey = Text(Point(350, 530), "Rank      |      Score    |      Player")
        titleKey.setSize(20)
        titleKey.draw(self.window)
        titleLine = Text(Point(350, 545), "------------------------------------------------------")
        titleLine.setSize(20)
        titleLine.draw(self.window)

        #Add all drawn objects to list so they can be deleted later
        self.hof_Objects.append(title)
        self.hof_Objects.append(titleKey)
        self.hof_Objects.append(titleLine)

        lineNum = 1
        pointY = 570
        for line in hof:
            self.__draw_HOF_line(lineNum, line[0], line[1], pointY)
            lineNum += 1
            pointY += 30

    def __draw_HOF_line(self, lineNum, score, player, pointY):
        textSize = 18
        rankX = 180
        scoreX = 350
        playerX = 515

        rank = Text(Point(rankX, pointY), lineNum)
        rank.setSize(textSize)
        rank.draw(self.window)

        scoreText = Text(Point(scoreX, pointY), score)
        scoreText.setSize(textSize)
        scoreText.draw(self.window)

        name = Text(Point(playerX, pointY), player)
        name.setSize(textSize)
        name.draw(self.window)

        #Add objects to list so they can be deleted later
        self.hof_Objects.append(rank)
        self.hof_Objects.append(scoreText)
        self.hof_Objects.append(name)
    
    #Name Entry Methods
    def draw_name_entry(self):
        #Draws the player name entry screen
        #Can draw here between y 550 and 650
        self.state.setNameEntry()
        x = 310
        y = 500
        width = 15
        inputBox = Entry(Point(x, y), width)
        inputBox.setSize(18)
        inputBox.setFill("light steel blue")
        inputBox.draw(self.window)

        enterX1 = x + 120
        enterX2 = x + 190
        ul = Point((enterX1), y-15)
        lr = Point((enterX2), y+14)
        enter = Rectangle(ul, lr)
        enter.setFill("lime green")
        enter.draw(self.window)
        #Add to dict to find if button clicked
        self.buttonsNE["Enter"] = [ul, lr]

        textPoint = Point((((enterX2-enterX1)/2)+enterX1), y)
        text = Text(textPoint, "Enter")
        text.setSize(18)
        text.draw(self.window)

        self.name_Objects.append(inputBox)
        self.name_Objects.append(enter)
        self.name_Objects.append(text)
    
    def get_name_entered(self):
        inputBox = self.name_Objects[0]
        name = inputBox.getText()
        return name
    





