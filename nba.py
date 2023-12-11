print("Loading Libraries . . . . . . . . . . . . . . . . . . . . . .")

from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.endpoints import franchisehistory
from nba_api.stats.endpoints import leagueleaders
from nba_api.stats.static import teams
from nba_api.stats.static import players   

from datetime import datetime, timezone
from dateutil import parser
from nba_api.live.nba.endpoints import scoreboard

import numpy
import pandas as pd
import pprint

print ("\nComplete\n")
nba_teams = teams.get_teams()
nba_players = players.get_players()

def fetch_data(x):
    """
    Returns nba player or team ID based on given team or player details.
    
    Accepts full team names, abbreviated names, team cities, states, or nicknames
    """
    input = x.lower()
    for team in nba_teams:
        for key, value in team.items():
            if str(value).lower() == input:
                return 'team', team['id']
    for player in nba_players:
        for key, value in player.items():
            if str(value).lower() == input:
                return 'player', player['id']
    return None
    
# print(fetch_data('bos'))

def process_data(id):
    """
    Takes a nba player or team ID and performs statistical analysis on chosen nba player or team data
    """
    if id[0] == 'player':
        player = playercareerstats.PlayerCareerStats(player_id=f"{id[-1]}") # draws specific player's data
        player = player.get_data_frames()[0] # generates pandas data frame
        return player
    elif id[0] == 'team':
        team = franchisehistory.FranchiseHistory() # draws all teams' data
        team = team.get_data_frames()[0] # generates pandas data frame
        team = team.loc[(team['TEAM_ID'] == id[-1])] # selects specific team
        team = team.iloc[0] # narrows to the first iteration of the team
        team = team[
            ['TEAM_CITY', 'TEAM_NAME', 'GAMES', 'WINS', 'LOSSES', 'WIN_PCT', 'PO_APPEARANCES', 'CONF_TITLES', 'START_YEAR']
            ] # narrows data frame to only needed data points
        return team
    else:
        return None


print(process_data(fetch_data('lakers')))

# print(process_data(('player', 2544)))

def generate_report(data):
    """
    Generates a visual report of compiled statistics
    """
    pass

def live_games():
    """
    Prints today's nba scheduled games
    """
    f = "{awayTeam} vs. {homeTeam} @ {gameTimeLTZ}" 
    board = scoreboard.ScoreBoard()
    print(f"\nNBA Schedule for: {board.score_board_date}")
    games = board.games.get_dict()
    num_of_games = 0
    for game in games:
        num_of_games += 1
        gameTimeLTZ = parser.parse(game["gameTimeUTC"]).replace(tzinfo=timezone.utc).astimezone(tz=None)
        print(f.format(gameId=game['gameId'], awayTeam=game['awayTeam']['teamName'], homeTeam=game['homeTeam']['teamName'], gameTimeLTZ=gameTimeLTZ))
    # print(f"\n\nThere are {num_of_games} Games Today!")

def main():
    user_input = input("Enter team or player ID: ")
    raw_data = fetch_data(user_input)
    processed_data = process_data(raw_data)
    generate_report(processed_data)

# if __name__ == "__main__":
#     main()