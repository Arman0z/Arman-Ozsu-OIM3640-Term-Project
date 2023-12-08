print("Loading Libraries")
from nba_api.stats.endpoints import playercareerstats

from nba_api.live.nba.endpoints import scoreboard
from nba_api.stats.static import teams
from nba_api.stats.static import players   
import numpy
import pandas
import pprint

print ("\n\n\nBeg.\n\n\n")

# Nikola Jokić
nikolaJ = playercareerstats.PlayerCareerStats(player_id='203999') 

# Today's Score Board
games = scoreboard.ScoreBoard()

# json
games.get_json()

# dictionary
games.get_dict()

ad = playercareerstats.PlayerCareerStats(player_id="203076")
print(ad.get_data_frames()[0])

# get_teams returns a list of 30 dictionaries, each an NBA team.
nba_teams = teams.get_teams()
print("Number of teams fetched: {}".format(len(nba_teams)))
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
print(big_fundamental)

print ("\n\n\nEnd.")