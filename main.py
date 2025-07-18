import os

# Directory stuff to prepare for opening
_directoryStr = "Lists"
_directory = os.fsencode(_directoryStr)
_endFile = "List_of_cards.csv"

# Global information about parameters for sanitising
_amountOfDecks = 32
_archetypes = {"Ignister", "Maliss", "Mitsurugi", "Vanquish Soul", "Memento", "Orcust", "Lunalight", "Gem-Knight", "Ryzeal", "Blue-Eyes", "Goblin Biker", "Mermail", "Atlantean", "P.U.N.K.", "White Forest", "Fiendsmith"}

# ReadList
# Input: none
# Output: Dictionary in the form "cardName: amount"
def ReadList():
    print("Making temp dict")
    tempDict = dict()
    
    print("Reading lists")
    for file in os.listdir(_directory):
        fileName = os.fsdecode(file)
        print("Reading " + fileName)
        with open(_directoryStr + "/" + fileName) as fp:
            for line in fp:
                # Check if line is valid
                if line[0] not in ('1','2','3'):
                    continue
                
                # Yoink amount
                amount = int(line[0])

                # Check if card is already in list
                cardName = line[2:len(line)-1]

                # If yes, simply add to the number
                if cardName in tempDict.keys():
                    print(cardName + " already exists")
                    newAmount = tempDict[cardName] + amount
                    tempDict[cardName] = newAmount
                    print(cardName + " updated")
                    continue

                # Otherwise, add the card
                tempDict[cardName] = int(amount)
    
    return tempDict

# Sanitising dictionary by dividing the number of copies by the number of decks and removing most normal engine pieces
# SanitiseDict
# Input: Un-sanitised dictionary
# Output: Sanitised dictionary, ie with main archetype cards removed and with amount divided by amount of decks
def SanitiseDict(rawDict):
    print("Sanitising dictionary")
    keyList = list(rawDict.keys())
    for kp in keyList:
        # Check string with find
        is_archetype = False
        for a in _archetypes:
            if kp.find(a) != -1:
                rawDict.pop(kp)
                is_archetype = True
                continue
        
        if is_archetype:
            continue

        rawDict[kp] = rawDict[kp] / _amountOfDecks
    

    return rawDict
        
# WriteIntoFile
# Input: The dictionary containing card data, string for the csv file to write to
# Output: None
def WriteIntoFile(endDict, endFileStr):
    print("Writing into end file")
    with open(endFileStr, "w") as fp:
        for kp, vp in endDict.items():
            lineToWrite = kp + ";" + str(vp) + "\n"
            fp.write(lineToWrite)


def main():
    # Count in each file
    rawDict = ReadList()

    # Sanitise the input a lil
    endDict = SanitiseDict(rawDict)

    # Create the file for full list and write into it
    WriteIntoFile(endDict, _endFile)


if __name__ == "__main__":
    main()