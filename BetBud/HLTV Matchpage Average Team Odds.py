"""
TODO:
1. Copy from value calculator.py to functions?
2. Expand implied odds into true_implied_odds calculating implied odds minus the bookie margin
2. Object oriented - needed as average odds needs to be calculated first - ask andreas about this
Have average odds or each function as its own class? - import all functions into one main script so its clean. How to approach this?
Have one file with all functions - Import an run them on a main script which is responsible for taking in HLTV matchpage?/
3. Asyncio - needs to calculate average odds to use value functions
4. Work out how the main() will work. It has to store results of certain functions before others can be run
5. BS4 Stuff - see below
6. Error handling - Try, except statements, combined with Ascyncio(needed for web stuff anyway)
7. In the future filter games further and include bet amount as units (percentage of bank roll) - need to ask an experienced better for more advice on calculating this
8. Store results in your own MySQL DB - Paper trade - profit over time when betting on all games above certain +EV starting BR 100?
9. Take out odd margins to find true odds instead of building your own modeling system
LAST STEP. DISCORD BOT? | In discord bot part only display games that have a positive expected value betting x units


BS4/SCRAPY STUFF:
use web var here with bs4 to check if a game is upcoming/live/over first before running the average odds calculation below
can check timer where it says 'LIVE' when a game is upcoming to check if its coming in < 1 hour
use web var with bs4 to get 'Pick a winner' values to compare upcoming games to implied odds <<< - IMPORTANT
have the bs4 checks as functions and the requests as the __INIT__ feeding in the matchpage var
Asyncio - Will at least be needed for web scraping.
Use BS4 for basic information to add to the games, such as checks if its bo1, bo3, time to match, upcoming, finished etc.
MLB / NBA lines too efficient (for basic model) - Book has all the data you do and more + the resources to use it well.
Save all the webpages you scrape to a database before you scrape. Keep your own waybackmachine.
Dictionary function (NLTK? NAtural language processing) to deal with mislabeled data on sites.

BUILD A MODEL TO GET YOUR OWN PREDICTIONS:
1. Requests & Scrapy + Proxy support for scraping HLTV a lot
2. Bayseian Model - Basic classification first, walk before you run.

BETTING WITHOUT A MODEL EXPLOITING BOOKIES:
1. http://www.football-data.co.uk/The_Wisdom_of_the_Crowd_updated.pdf
2. Finding the 'true' odds minus the 4-10% margin in the odds (creating games with implied odds over 100%)
3. Looking for holes in soft bookies exploiting the true odds

"""

import ValueCalculator
import pandas as pd
import requests
from collections import namedtuple


# Hardcoded HLTV Matchpage to be replaced with scrapy/bs4
HLTV_MATCHPAGE = "https://www.hltv.org/matches/2335653/avangar-vs-astralis-starladder-major-berlin-2019"


def find_average_odds(matchpage):

    # Uses requests package to get the website data and save it to web var
    web = requests.get(matchpage)


    dfs = pd.read_html(web.text)
    # Uses pandas .read_html() function to read data saved to web var. (remember to use .text)
    # Returns it as dataframe(s!) as a list of dataframes based on all the tables it finds.

    # Show all dataframes found on the page - Debugging purposes
    # for df in dfs:
    #     print(df.head())

    # Copy the DF and set team names
    df = dfs[0].copy()
    team1 = df.at[0, 1]
    team2 = df.at[0, 3]

    # Delete unused columns of DF
    del df[0]
    del df[2]

    # Convert columns to numeric values (float) force non-numeric to NaN
    df[1] = pd.to_numeric(df[1], errors='coerce')
    df[3] = pd.to_numeric(df[3], errors='coerce')

    # Drop NaN rows
    df.dropna(axis=0, inplace=True)

    # Calculate average odds
    team1_average_odds = df[1].mean()
    team2_average_odds = df[3].mean()
    team1_average_odds = round(team1_average_odds, 2)
    team2_average_odds = round(team2_average_odds, 2)
    # return team1_average_odds, team2_average_odds

    # Named tuple for return
    Teams = namedtuple('Teams', 'name odds')
    team_tuple1 = Teams(team1, team1_average_odds)
    team_tuple2 = Teams(team2, team2_average_odds)

    return team_tuple1, team_tuple2

# Running the script - main() in future
team1, team2 = find_average_odds(HLTV_MATCHPAGE)
team1_implied_value = ValueCalculator.get_implied_value(team1)
team2_implied_value = ValueCalculator.get_implied_value(team2)

odds_margin = ValueCalculator.odds_margin(team1, team2)

team1_true_prob = team1_implied_value / (odds_margin + 1)
team2_true_prob = team2_implied_value / (odds_margin + 1)
team1_true_prob = round(team1_true_prob, 2)
team2_true_prob = round(team2_true_prob, 2)

team1_true_decimal = (100 / team1_true_prob) / 100
team2_true_decimal = (100 / team2_true_prob) / 100

team1_kelly = ValueCalculator.kelly_criterion(team1, team1_true_prob)
team2_kelly = ValueCalculator.kelly_criterion(team2, team2_true_prob)


# Print results
print(team1, team2)
print("Current {} implied percent is {}%. Current {} implied percent is {}%".format(team1.name, team1_implied_value,
                                                                                    team2.name, team2_implied_value))
print("Current implied percentage including the betting margin {}%".format(odds_margin))
print("{} true probability is {}%".format(team1.name, team1_true_prob * 100))
print("{} true probability is {}%".format(team2.name, team2_true_prob * 100))
print("{} true decimal is {}".format(team1.name, team1_true_decimal))
print("{} true decimal  is {}".format(team2.name, team2_true_decimal))
print("{} kelly is {} Units".format(team1.name, team1_kelly))
print("{} kelly is {} Units".format(team2.name, team2_kelly))


# Examples:
# team1, team2 = find_average_odds()
# team1_get_implied_value = ValueCalculator.get_implied_value(team1)
# print(team1_get_implied_value)