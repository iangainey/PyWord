'''
This class is for grid objects. These are the "cubes" seen on the screen that 
letters guessed are placed in, and change color once a guess is entered depending
on the correctness of the letter.
It is used by gui.py
'''

class Grid:
    
    def __init__(self) -> None:
        self.ul = 0
        self.lr = 0
        self.gridObj = ""