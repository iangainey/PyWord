import string
import hall_of_fame as HOF
import word_bank as WB

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

    def main_menu(self):
        #Prints out the main menu, gets user input for a choice, calls proper functions
        
        print("Welcome to PyWord.")

        while True:
            print("")
            print("----- Main Menu -----")
            print("1. New Game")
            print("2. See Hall of Fame")
            print("3. Quit")
            print("")

            choice = input("What would you like to do? ")

            if (choice == "1"):
                self.__game()
                self.__reset_game()
            
            elif (choice == "2"):
                self.hof.print_HOF()
                

            elif (choice == "3"):
                print("Goodbye.")
                return
            
            else:
                print("")
                print("Invalid choice. Please try again.")

    def __game(self):
        #Set up game, calls the rounds, and outputs information after round
        
        secretWords = self.wordBank.pick_game_words()

        self.name = input("Enter your player name: ")

        for i in range(0, self.rounds):
            self.score += self.__play_round(secretWords)
            self.round += 1
        
        self.hofEntry.append(str(self.score))
        self.hofEntry.append(self.name)

        #Get true or false if added to hall of fame:
        hofWorthy = self.hof.compare_HOF(self.hofEntry)

        if hofWorthy:
            print("")
            print(f"Way to go {self.name}!")
            print(f"You earned a total of {self.score} points and made it into the Hall of Fame!")
            self.hof.print_HOF()
    
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

    def __play_round(self, secretWords):
        #Play one round. Only called by game(). Returns a score obtained in the round
        word = secretWords[(self.round-1)]

        guessSummary = []
        guessRecord = [" "]*26
        

        print("")
        print(f"Round {self.round}:")

        for i in range(1, 7):

            while True:
                guess = input(f"{i}? ")
                guess = guess.lower()

                if (self.words.count(guess)):
                    break

                elif (len(guess) > 5 or len(guess) < 5):
                    print("")
                    print("Invalid guess. Please enter exactly 5 characters.")
                    print("")
                
                elif (i in guess for i in string.punctuation):
                    print("")
                    print("Invalid guess. Please only enter letters")
                    print("")

            #Compare guess, get output and update guessRecord
            output, guessRecord = self.wordBank.compare_words(guess, word, self.guessLibrary, guessRecord)
            #Guess record is a list, use a string to display it properly
            guessRecordString = ""
            for symbol in guessRecord:
                guessRecordString += symbol
            #Print output followed by current guessRecord on same line
            print(f"   {output}", end = '')
            print(f"     {guessRecordString}")
            #Print the current secret word and alphabet(library) on same line
            print(f"   {word}", end = '')
            print(f"     {self.guessLibrary}")

            #If word is guessed, get score, print score and summary, and return point value to start next round
            if (output == "!!!!!"):
                accolade, points = self.__get_accolades(i)
                print(f"{accolade}! You earned {points} points this round.")
                self.__print_round_summary(guessSummary, output)
                return points
            #If it's not guessed, add the current guess correctness to the summary
            else:
                guessSummary.append(output)
        
        #If for loop exits without returning points, word was never guessed in round
        #Print the word, the summary, and return 0 points for round
        print("You ran out of tries.")
        print(f"The word was {word}.")
        self.__print_round_summary(guessSummary, output)
        points = 0
        return points

    def __print_round_summary(self, guessSummary, output):
        #Prints the round summary of guesses
        print(f"Round {self.round} summary:")
        guessSummary.append(output)
        for guesses in guessSummary:
            print(f"   {guesses}")

    def __reset_game(self):
        self.name = ""
        self.score = 0
        self.round = 1
        self.hofEntry = []