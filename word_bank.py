import random
import pyword_game as gm

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

    #def compare_words(self, guess, word, guessLibrary, guessRecord):
    def compare_words(self, guess, word):
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
                    #guessRecord[(guessLibrary.index(letter))] = "!"
                else:
                    #Letter is in word, not in right place
                    output += "?"
            else:
                #Letter is not in word
                output += "X"

        #Before returning, need to check if there are duplicates 
        #i.e. a letter marked correct in one spot, and the same letter guessed in another spot marked yellow even when there's only 1 in word
        
        #Check if there are more than 1 instance of a letter in guess
        for letter in guess:
            if guess.count(letter) > 1:
                #More than 1 instance of letter in guess
                #Check if there is more than 1 in word
                if word.count(letter) > 1:
                    #There is more than 1 in word and more than 1 in guess, probably marked correctly
                    pass
                else:
                    #Not more than 1 in word, one was probably marked incorrectly

                    #Find if one was marked as "!", if so find the other and mark as "X"
                    foundFirst = False
                    for index, l in enumerate(guess):
                        if (l == letter):
                            #Find what it's marked as in output
                            if (output[index] != "!"):
                                #If it's not marked as correct in output, mark as X
                                output = output[:index] + "X" + output[index+1:]
                            #Find if both were marked as "?", if so find the 2nd one and mark as "X"
                            elif (output[index] == "?"):
                                if (foundFirst):
                                    #This is a duplicate
                                    output = output[:index] + "X" + output[index+1:]
                                else:
                                    foundFirst == True
            else:
                #Not more than 1, so disregard
                pass

        #return output
        return output