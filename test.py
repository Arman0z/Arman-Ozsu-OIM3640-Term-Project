print("Loading Libraries . . . . . . . . . . . . . . . . . . . . . .")

from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.endpoints import leagueleaders
from nba_api.stats.static import teams
from nba_api.stats.static import players   

from datetime import datetime, timezone
from dateutil import parser
from nba_api.live.nba.endpoints import scoreboard

import re

import numpy
import pandas as pd
import pprint

print ("\n\n\nDone Loading Libraries . . . . . . . . . . . . .\n\n\n")

# Nikola Jokić
nikolaJ = playercareerstats.PlayerCareerStats(player_id='203999') 

ll = leagueleaders.LeagueLeaders(league_id='00')
ll_df = ll.get_data_frames()[0]
print (ll_df)
ll_df = ll_df [["PLAYER", "TEAM", "PTS"]]
ll_10_df = ll_df.head(11)
# print(ll_df.groupby(['TEAM']).mean())
# print(ll_df.loc('TEAM'))

# Today's Score Board
games = scoreboard.ScoreBoard()

# dictionary
games.get_dict()


# get_teams returns a list of 30 dictionaries, each an NBA team.
nba_teams = teams.get_teams()
print(f"Number of teams fetched: {len(nba_teams)}")
nba_teams[:3]
print(nba_teams)

nba_players = players.get_players()
print("Number of players fetched: {}".format(len(nba_players)))
nba_players[:5]
# print(nba_players)

spurs = [team for team in nba_teams if team["full_name"] == "San Antonio Spurs"][0]
print(spurs)

big_fundamental = [
    player for player in nba_players if player["full_name"] == "Tim Duncan"
][0]
# print(big_fundamental)


#TODO Anthony Davis Dataframe example:
ad = playercareerstats.PlayerCareerStats(player_id="203076")
ad_df = ad.get_data_frames()[0] #! Gets Player Data_Frame
ad_df = ad_df[['TEAM_ABBREVIATION', 'SEASON_ID', 'PTS', 'REB', 'MIN']]
ad_df['PTS/MIN'] = ad_df['PTS'] / ad_df['MIN']
ad_df['PTS/MIN'] = ad_df['PTS/MIN'].round(2)
print(ad_df)

#TODO Live Games
f = "{awayTeam} vs. {homeTeam} @ {gameTimeLTZ}" 
board = scoreboard.ScoreBoard()
print(f"\nNBA Schedule for: {board.score_board_date}")
games = board.games.get_dict()
num_of_games = 0
for game in games:
    num_of_games += 1
    gameTimeLTZ = parser.parse(game["gameTimeUTC"]).replace(tzinfo=timezone.utc).astimezone(tz=None)
    print(f.format(gameId=game['gameId'], awayTeam=game['awayTeam']['teamName'], homeTeam=game['homeTeam']['teamName'], gameTimeLTZ=gameTimeLTZ))
print(f"\n\nThere are {num_of_games} Games Today!")

from nba_api.live.nba.endpoints import boxscore
box = boxscore.BoxScore('0022000196') 
box.game.get_dict()
print(box)






print ("\n\n\nEnd.")