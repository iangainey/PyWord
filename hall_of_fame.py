
class hall_of_fame:

    def __init__(self) -> None:
        pass

    def load_HOF(self) -> list:
        #Loads hall of fame, returns as a list with each element containing [score][name]
        lines = ""
        with open("hall_of_fame.txt") as file:
            lines = file.readlines()
        #score, name is format of each line read
        hof = []
        for line in lines:
            #Split up score and name get just the needed info
            line = line.strip()
            lineWords = line.split(", ")
            #Ensure list is not empty, lineWords returns false if empty
            if lineWords:
                hofLine = [] #Create a new line for hof
                hofLine.append(lineWords[0]) #appends score to the line
                hofLine.append(lineWords[1]) #appends name to the line
                hof.append(hofLine)
        return hof

    def compare_HOF(self, entry):
        #Called to determine if an entry can be placed in hall of fame. 
        #Calls update_HOF() and returns true if so, otherwise returns false

        hof = self.load_HOF()

        if not hof:
            #If hof is currently empty, add entry to index 0
            hof.append(entry)
            self.__write_HOF(hof)
            return True
        
        #Search hof for a value that is less than current score
        #Entry = score, player
        newScore = int(entry[0])
        for index, line in enumerate(hof):
            currScore = int(line[0])

            if (newScore > currScore):
                #New entry to add
                insertIndex = hof.index(line)
                hof.insert(insertIndex, entry)
                self.__write_HOF(hof)
                return True  
            elif (newScore == currScore):
                #New entry to add, but this should go below previous equal score
                #Check to ensure next element isn't the same value. If so, do nothing.
                #Will be taken care of as it iterates through until it reaches one where next
                #element is not the same value
                #Equals
                if (index < (len(hof) -1)):
                    #Check to ensure current ele is not last
                    nextEle = hof[index+1]
                    if (int(nextEle[0]) != newScore):
                        #If next ele is not same score, insert here
                        insertIndex = hof.index(line)
                        hof.insert((insertIndex + 1), entry)
                    else:
                        continue #Continue until next score is not the same
                else:
                    #if it is last element, add it here
                    if (len(hof) < 10):
                        #If it will not overflow hof, append
                        hof.append(entry)
                    else:
                        #If hall of fame is full, and new score is equal to the last score
                        #in hof, entry does not actually make hof, so return false
                        return False

                self.__write_HOF(hof)
                return True
            
        #After going through all of the current scores in HOF:
        if (len(hof) < 10):
            #If hall of fame isn't full, and not higher or equal to others, add to end
            hof.append(entry)
            self.__write_HOF(hof)
            return True

        #If none of above have returned true, return false
        return False

    def __write_HOF(self, hof):
        #Writes an updated hall of fame back to the hof file
        #Only should be called from compare_HOF()
        if (len(hof) > 10):
            hof.pop()
        newHOF = []
        for line in hof:
            newLine = line[0] + ", " + line[1] + "\n"
            newHOF.append(newLine)
        
        with open('hall_of_fame.txt', 'w') as file:
            file.writelines(newHOF)
        
