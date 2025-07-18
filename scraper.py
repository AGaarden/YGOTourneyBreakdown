import requests

def ScrapeTourney():
    tourney_url = "https://ygoprodeck.com/tournament/north-america-wcq-2025-3208"
    endFileStr = "Scraper_Saves/Tourney_Data.txt"
    
    response = requests.get(tourney_url)
    
    if response.status_code == 200:
        with open(endFileStr, "w") as fp:
            fp.write(response.text)

def ScrapeDeck():
    deck_url = "https://ygoprodeck.com/deck/fiendsmith-orcust-621537"
    endFileStr = "Scraper_Saves/Deck_Data.txt"

    response = requests.get(deck_url)
    
    if response.status_code == 200:
        with open(endFileStr, "w") as fp:
            fp.write(response.text)

# Extra functions:
# Separate main from extra from side
  # Find the spot it says main, extra, side, separate out
# find flags for cards


def main():
    print("Test")
    # def ScrapeTourney()
    # def ScrapeDeck()
    

if __name__ == "__main__":
    main()