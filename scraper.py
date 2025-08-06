import requests
from sys import exit
from dataclasses import dataclass

# This class holds onto dictionaries for all the available decks, as well as 
@dataclass
class Tournament:
    mainDeck: dict
    extraDeck: dict
    sideDeck: dict
    deckCount: int

_tourneyURL = "https://ygoprodeck.com/tournament/north-america-wcq-2025-3208" # Hardcoded tournament for now

# ScrapeTourneySite
# Input: URL to scrape
# Output: List of URL's to scrape decks from, and amount of decks at final entry of list
def ScrapeTourneySite(url):
    response = requests.get(url)
    
    # If the code returns any data, HTML code 200 is OK
    if response.status_code == 200:
        # Start looping through response.text, which is a string version of the page data
        startIndex = 0
        amountOfDecks = 0
        deckURLs = []
        # This loop runs through the string starting from 0 or the first instance of "data-deckurl="", and adds URLs to the list until there is none more
        while True: 
            startIndex = response.text.find("data-deckurl=\"", startIndex)
            if startIndex == -1: 
                deckURLs.append(str(amountOfDecks)) # Amount of decks in final index of the list
                break # If the text is done being looped through, find returns -1
            link = "https://ygoprodeck.com" + response.text[startIndex+14:response.text.find("\"", startIndex+14)]
            deckURLs.append(link)
            amountOfDecks += 1
            startIndex += len("data-deckurl=\"")

        print("Tournament site scraped")
        return deckURLs
    else:
        print("Failed to retrieve data from tournament site")
        exit()

# ScrapeDeck
# Input: URL to scrape
# Output: Dictionaries for main, extra, and side deck, with amounts for each cards
def ScrapeDeck(url):
    response = requests.get(url)
    
    # If the code returns any data, HTML code 200 is OK
    if response.status_code == 200:
        # Find relevant indices
        mainDeckIndex = response.text.find("main_deck")
        extraDeckIndex = response.text.find("extra_deck")
        sideDeckIndex = response.text.find("side_deck")

        # Grab decks into separate string, initialise the end data
        mainDeckRaw = response.text[mainDeckIndex:extraDeckIndex]
        extraDeckRaw = response.text[extraDeckIndex:sideDeckIndex]
        sideDeckRaw = response.text[sideDeckIndex:]
        mainDeckData = dict()
        extraDeckData = dict()
        sideDeckData = dict()

        # 
        for raw, end in [(mainDeckRaw, mainDeckData), (extraDeckRaw, extraDeckData), (sideDeckRaw, sideDeckData)]:
            # print(raw[:5] + end[0])

            startIndex = 0
            # This loop runs through the string starting from 0 or the first instance of "data-cardname="", and adds cards to the data dictionary as necessary
            while True:
                startIndex = raw.find("data-cardname=\"", startIndex)
                if startIndex == -1: 
                    break # If the text is done being looped through, find returns -1
                card = raw[startIndex+15:raw.find("\"", startIndex+15)]
                
                if card.find("amp;") != -1:
                    card = card[:card.find("amp;")] + card[card.find("amp;")+4:]

                # If card is already in dictionary, +1 instead
                if card in end.keys():
                    end[card] += 1
                else:
                    end[card] = 1

                startIndex += len("data-cardname=\"")
        
        return mainDeckData, extraDeckData, sideDeckData
    else:
        print("Failed to retrieve data from tournament site")
        exit()


# ScrapeTournament
# Input: A URL for a tournament
# Output: 3 dictionaries with main, extra, and side deck cards, as well as frequency
def ScrapeTournament(tourneyURL):
    # Initialise tournament
    tourney = Tournament(dict(), dict(), dict(), 0)

    # deckURLs = ScrapeTourneySite(tourneyURL)
    deckURLs = ["https://ygoprodeck.com/deck/ignister-maliss-621538", "https://ygoprodeck.com/deck/ignister-maliss-621539", 2]
    tourney.deckCount = deckURLs[-1] # Put number of decks into the tournament

    # Get all data for the decks out and loop through, to add up for end
    # Ignore last due to this being number of decks
    for URL in deckURLs[:-1]:
        mainDeckCards, extraDeckCards, sideDeckCards = ScrapeDeck(URL)

        # For each corresponding deck (main, extra, side)
        for deck, end in [(mainDeckCards, tourney.mainDeck), (extraDeckCards, tourney.extraDeck), (sideDeckCards, tourney.sideDeck)]:
            # For each card in the dictionary from ScrapeDeck
            for card in deck.keys():
                # If card is already in dictionary, add them up
                if card in end.keys():
                    newAmount = end[card] + deck[card]
                    end[card] = newAmount
                    continue
                else:
                    end[card] = deck[card]
    
    return tourney