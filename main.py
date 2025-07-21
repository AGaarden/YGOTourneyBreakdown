import os
import scraper
import test_functions as tf

_tourneyURL = "https://ygoprodeck.com/tournament/north-america-wcq-2025-3208" # Hardcoded tournament for now

# Directory stuff to prepare for opening
_directoryStr = "Lists"
_directory = os.fsencode(_directoryStr)
_endFile = "output/List_of_cards.csv"
_endFileNoExt = "output/List_of_cards"
_endSanFileNoExt = "output/List_of_cards_san"

# Global information about parameters for sanitising
_archetypes = {"Ignister", "Maliss", "Mitsurugi", "Vanquish Soul", "Memento", "Orcust", "Lunalight", "Gem-Knight", "Ryzeal", "Blue-Eyes", "Goblin Biker", "Mermail", "Atlantean", "P.U.N.K.", "White Forest", "Fiendsmith"}

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

def main():
    # Get tourney file
    #tourney = scraper.ScrapeTournament(_tourneyURL)
    tourney = tf.ReadSavedData()
    tourney.deckCount = 2

    # Sanitise the input
    tourney = SanitiseTourney(tourney)

    # Create the file for full list and write into it
    tf.WriteTourneyIntoFileTest(tourney, _endSanFileNoExt)
    # WriteTourneyIntoFileTest(tourney, _endFileNoExt)

if __name__ == "__main__":
    main()