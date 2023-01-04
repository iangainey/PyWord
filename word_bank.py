import random

class word_bank:

    def __init__(self) -> None:
        pass

    def get_word_bank(self):
        #Loads word bank from file, formatting via stripping and lowercasing. Returns
        #a list of words from the file
        words = []

        with open('words.txt') as file:
            wordTxt = file.readlines()
        
        for word in wordTxt:
            word = word.strip()
            word = word.lower()
            words.append(word)

        return words

    def pick_game_words(self):
        #Picks 3 unique words from the bank. Return these words as a list
        
        words = self.get_word_bank()

        gameWords = []

        for word in range(3):
            word = random.choice(words)
            words.remove(word)
            gameWords.append(word)

        return gameWords 

    def compare_words(self, guess, word, guessLibrary, guessRecord):
        #Compares a guess to the current secret word. Returns indication of letter correctness,
        #as well as updating guess library

        # ! = Correct Letter & Position
        # ? = Correct Letter, Wrong Position
        # X = Wrong all over

        output = ""
        for index, letter in enumerate(guess):
        #Check if letter is in word
            if (word.count(letter)):
            #If letter is in word, check if in correct place
                if (word[index] == letter):
                    #If letter is in word and in correct place, !
                    output += "!"
                    guessRecord[(guessLibrary.index(letter))] = "!"
                else:
                    #Letter is in word, not in right place
                    output += "?"
                    if (guessRecord[(guessLibrary.index(letter))] != "!"):
                        guessRecord[(guessLibrary.index(letter))] = "?"
            else:
                #Letter is not in word
                output += "X"
                guessRecord[(guessLibrary.index(letter))] = "X"

        return output, guessRecord
