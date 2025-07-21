import os
import scraper

# This function only exists to make data to test on without having to constantly call on lots of requests on poor YGOProdeck.com
def WriteTourneyIntoFileTest(tourney, endFileStr):
    print("Writing into end files")

    count = 1
    for deck in [tourney.mainDeck, tourney.extraDeck, tourney.sideDeck]:
        fileStr = endFileStr + "_" + str(count) + ".csv"
        with open(fileStr, "w") as fp:
            fp.write("Deck count: " + str(tourney.deckCount) + "\n")

            for kp, vp in deck.items():
                lineToWrite = kp + ";" + str(vp) + "\n"
                fp.write(lineToWrite)
        
        count += 1
      
def ReadSavedData():
    tourney = scraper.Tournament(dict(), dict(), dict(), 0)

    for file in os.listdir(os.fsencode("output")):
        fileName = os.fsdecode(file)
        print("Reading " + fileName)
        with open("output/" + fileName) as fp:
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