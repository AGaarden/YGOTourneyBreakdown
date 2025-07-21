# YGOTourneyBreakdown
A Python script scraping YGOProDeck.com tournament pages and summarising various informations.

The current functionality of this program is averaging and summarising non-engine (ie non-archetype related) cards of Yu-Gi-Oh decks such that the average amount of cards in the population is known. This is currently limited to manually inserted decklists, no command line inputs, and thus manual changing of the code to ensure things work. 

TODO: 
- Make user input such that the following can be picked and chosen at will:
  - Inputting a tournament link to not require hardcoding
    - Needs more error handling to make sure an input tournament doesn't just start running amok
  - Specific deck types present in this tournament
  - Only some amount of the top is chosen, ie top 4, top 8, top 16, etc
  - Whether only non-engine is included
