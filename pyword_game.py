import string
import hall_of_fame as HOF
import word_bank as WB
from gui.gui import GUI

'''
Current Objectives:

1. Add key entering functionality, not just mouse clicking 

2. Redo some features. Some can be grouped together/improved
    A. 
'''
class pyword_game:
    
    def __init__(self) -> None:
        self.hof = HOF.hall_of_fame()
        self.wordBank = WB.word_bank()
        self.words = self.wordBank.get_word_bank()
        self.name = ""
        self.score = 0
        self.round = 1
        self.rounds = 3
        self.hofEntry = []
        self.guessLibrary = "abcdefghijklmnopqrstuvwxyz"
        self.window = GUI()


    def main_menu(self):
        #Prints out the main menu, gets user input for a choice, calls proper functions
        while True:
            choice = self.window.main_menu()
            if choice == "New Game":
                self.window.undraw(choice) #Called to clear the display
                self.__game()
                self.__reset_game()
            elif choice == "Hall of Fame":
                self.window.undraw(choice) #Call to clear the display
                hof = self.hof.load_HOF()
                self.window.draw_HOF(hof)
            elif choice == "Quit":
                return
            else:
                print("Invalid choice. Please try again.")

    def __get_player_name(self):
        #Draws player name input screen and gets a name to assign to self.name
        self.window.draw_name_entry()
        while True:
            selection = self.window.get_selection()
            if (selection == "Enter"):
                while True:
                    self.name = self.window.get_name_entered()
                    if self.name != "":
                        break
                    else:
                        self.window.draw_game_text("Enter a name to continue")
                self.window.undraw(selection)
                return

    def __game(self):
        #Set up game, calls the rounds, and outputs information after round
        secretWords = self.wordBank.pick_game_words()

        self.__get_player_name() #Pauses until a name is entered
        
        #Play rounds
        for i in range(0, self.rounds):
            self.score += self.__play_round(secretWords)
            self.round += 1
        #Rounds are over, game is complete, undraw
        self.window.undraw("Game")
        
        self.hofEntry.append(str(self.score))
        self.hofEntry.append(self.name)

        #Get true or false if added to hall of fame:
        hofWorthy = self.hof.compare_HOF(self.hofEntry)
        #If made it to hall of fame, says how many points
        if hofWorthy:
            text = "You earned " + str(self.score) + " points and made it into the Hall of Fame!"
            self.window.draw_game_text(text)
        else:
            text = "You earned " +str(self.score) + " points this game"
            self.window.draw_game_text(text)
    
    def __play_round(self, secretWords):
        #Play one round. Only called by game(). Returns a score obtained in the round

        #Draw necessary setup each round
        if self.round == 1:
            self.window.draw_round()

        word = secretWords[(self.round-1)]
        print(word)
        
        for i in range(1, 7):
            while True:
                #Get the guess. Get guess checks if it's a valid guess
                guess = self.__get_guess(i)
                
                #Call compare words to get a string of letter correctness
                output = self.wordBank.compare_words(guess, word)
                if (len(output) > 0):
                    #Shows that the word is a valid word from the wordbank
                    self.__update_guess(guess, output, i)
                    if (output == "!!!!!"):
                        #Correct guess
                        accolade, points = self.__get_accolades(i)
                        text = accolade + "! You earned " + str(points) + " points this round! Click anywhere to continue"
                        self.window.draw_game_text(text)
                        self.window.reset_round()
                        return points
                    else:
                        #Since its a valid guess, call clear_guess_letters so row can't be deleted
                        self.window.clear_guess_letters()
                        break #Get to next row
        
        #If loop exits without returning points, correct word was never guessed
        self.window.draw_game_text("You ran out of tries. Click to continue")
        self.window.reset_round()
        points = 0
        return points

    def __get_guess(self, currentRow):
        #Called by __play_round to get a single guess
        guess = ""
        while True:
            #Gets a button selected by user
            selection = self.window.get_selection()

            if selection == "Enter":
                #User hit enter, check to see if they filled out a whole word

                if len(guess) == 5:
                    #Valid length guess
                    guess = guess.lower()
                    if self.words.count(guess):
                        return guess
                    else:
                        #Not a valid word
                        self.window.draw_game_text("Not a valid word in this word bank. Click anywhere to continue")
                        continue
            elif selection == "Back":
                #Delete last entered key
                self.window.undraw_guess_letter()
                guess = guess[:-1]
            else:
                #User selected a letter, display it on next available box
                #And add to word they're constructing
                if len(guess) == 5:
                    #Can't add anymore letters to this row
                    continue

                guess += selection
                index = len(guess) 
                self.window.draw_guess_letter(currentRow, index, selection)

    def __update_guess(self, guess, output, currentRow):
        for index, symbol in enumerate(output):
            #Updates display of keyboard indicating correctness of guess
            #Updates display of guess grid indicating correctness of guess
            if symbol == "!":
                #Correct letter in correct place
                self.window.fill_grid_box(currentRow, index, "lime green")
                letter = guess[index]
                self.window.fill_key(letter, "lime green")
            elif symbol == "?":
                #Correct letter in word, but in wrong place
                self.window.fill_grid_box(currentRow, index, "khaki")
                letter = guess[index]
                self.window.fill_key(letter, "khaki")
            elif symbol == "X":
                #Letter is not in the word
                self.window.fill_grid_box(currentRow, index, "light gray")
                letter = guess[index]
                self.window.fill_key(letter, "light gray")

    def __get_accolades(self, attemptNum):
        #Returns the accolade and point value depending on which attempt the right guess is made
        accolades = {
            0 : [ "Impossible" , 64 ],
            1 : [ "Genius" , 32 ],
            2 : [ "Magnificent" , 16 ],
            3 : [ "Impressive" , 8 ],
            4 : [ "Splendid" , 4 ],
            5 : [ "Great" , 2 ],
            6 : [ "Phew" , 1 ]
        }
        return accolades[attemptNum]

    def __reset_game(self):
        #Called whenever returning to main menu to reset game
        self.name = ""
        self.score = 0
        self.round = 1
        self.hofEntry = []