'''
This class is used for the keys on the keyboard when in the game. 
It is used by gui.py. 
'''

class Keyboard:
    
    def __init__(self) -> None:
        self.letter = "" #Holds what letter this key is
        self.ul = 0
        self.lr = 0
        self.keyObj = ""
        self.letterObj = ""
        self.color = "white"