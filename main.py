import os
import scraper

_tourneyURL = "https://ygoprodeck.com/tournament/north-america-wcq-2025-3208" # Hardcoded tournament for now

# Directory stuff to prepare for opening
_directoryStr = "YGOoutput"
_directory = os.fsencode(_directoryStr)
_endSanFileNoExt = "YGOoutput/List_of_cards_san"

# Global information about parameters for sanitising
_archetypes = {"Ignister", "Maliss", "Mitsurugi", "Vanquish Soul", "Memento", "Orcust", "Lunalight", "Gem-Knight", "Ryzeal", "Blue-Eyes", "Goblin Biker", "Mermail", "Atlantean", "P.U.N.K.", "White Forest", "Fiendsmith"}

# Extra table for names of decks
_decks_enum = ["main", "extra", "side"]

def SanitiseTourney(tourney):
    print("Sanitising tournament info of engine")

    for deck in [tourney.mainDeck, tourney.extraDeck, tourney.sideDeck]:
        keyList = list(deck.keys())
        for kp in keyList:
            # Check string with find
            is_archetype = False
            for a in _archetypes:
                if kp.find(a) != -1:
                    deck.pop(kp)
                    is_archetype = True
                    continue
        
            if is_archetype:
                continue

            deck[kp] = deck[kp] / tourney.deckCount

    return tourney

# Function: WriteTourneyIntoFile
# Input: Tournament data, end string
# Output: None
def WriteTourneyIntoFile(tourney, endFileStr):
    print("Writing into end files")

    for count, deck in enumerate([tourney.mainDeck, tourney.extraDeck, tourney.sideDeck]):
        fileStr = endFileStr + "_" + _decks_enum[count] + ".csv"
        os.makedirs(os.path.dirname(fileStr), exist_ok=True)
        with open(fileStr, "w") as fp:
            fp.write("Deck count: " + str(tourney.deckCount) + "\n")

            for kp, vp in deck.items():
                lineToWrite = kp + ";" + str(vp) + "\n"
                fp.write(lineToWrite)

# Function: ReadSavedData
# Input: None
# Output: Tournament data
# Remarks: This function reads saved data from a tournament that has been saved prior, saving bandwidth on YGOPRODeck
def ReadSavedData():
    tourney = scraper.Tournament(dict(), dict(), dict(), 0)

    for file in os.listdir(_directory):
        fileName = os.fsdecode(file)
        print("Reading " + fileName)
        with open(_directoryStr + "/" + fileName) as fp:
            tempDict = dict()
            next(fp)
            for line in fp:
                cardName = line[:line.find(";")]
                cardAmount = line[line.find(";")+1:line.find(";")+2]
                tempDict[cardName] = int(cardAmount)
        
        index = int(fileName[fileName.rfind("_")+1:fileName.rfind("_")+2])
        if index == 1:
            tourney.mainDeck = tempDict
        if index == 2:
            tourney.extraDeck = tempDict
        if index == 3:
            tourney.sideDeck = tempDict
    
    return tourney

def main():
    tourneyURL = ""
    if os.path.isfile(_directoryStr + "/List_of_cards_san_main.csv") == False:
        while tourneyURL.find("ygoprodeck.com/tournament/") == -1:
            print("Please enter the link to a YGOPRODeck tournament page")
            tourneyURL = input()
        
        tourney = scraper.ScrapeTournament(tourneyURL)
        tourney = SanitiseTourney(tourney)
        WriteTourneyIntoFile(tourney, _endSanFileNoExt)
    else:
        print("A tournament report already exists in the output folder. Please remove before continuing.")
        exit()

def testmain():
    if os.path.isfile(_directoryStr + "/List_of_cards_san_1.csv"):
        print("do thing")

    # Get tourney file
    #tourney = scraper.ScrapeTournament(_tourneyURL)
    tourney = ReadSavedData()
    tourney.deckCount = 2

    # Sanitise the input
    tourney = SanitiseTourney(tourney)

    # Create the file for full list and write into it
    WriteTourneyIntoFile(tourney, _endSanFileNoExt)
    # WriteTourneyIntoFileTest(tourney, _endFileNoExt)

if __name__ == "__main__":
    main()