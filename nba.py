from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.endpoints import franchisehistory
from nba_api.stats.static import teams
from nba_api.stats.static import players

from datetime import datetime, timezone
from dateutil import parser
from nba_api.live.nba.endpoints import scoreboard

import pandas as pd
import datetime

nba_teams = teams.get_teams()
nba_players = players.get_players()


def identify_subject(x):
    """
    Returns nba player or team ID based on given team or player details.

    Accepts full team names, abbreviated names, team cities, states, or nicknames
    for EITHER team names or player names!
    """
    input = x.lower()  # sets everything to lower case
    for team in nba_teams:  # searches list of all teams for a match
        for key, value in team.items():
            if str(value).lower() == input:
                return "team", team["id"]
    for player in nba_players:  # searches list of all players for a match
        for key, value in player.items():
            if str(value).lower() == input:
                return "player", player["id"]
    return None


def fetch_data(id):
    """
    Takes a nba player or team ID and generates pandas dataframe on chosen nba player or team data
    """
    if id[0] == "player":
        player = playercareerstats.PlayerCareerStats(
            player_id=f"{id[-1]}"
        )  # draws specific player's data
        player = player.get_data_frames()[0]  # generates pandas data frame
        player["AVG_PTS"] = player["PTS"] / player["GP"]  # creates new column
        player["AVG_PTS"] = player["AVG_PTS"].round(0)
        player["AVG_REB"] = player["REB"] / player["GP"]  # creates new column
        player["AVG_REB"] = player["AVG_REB"].round(0)
        player["AVG_AST"] = player["AST"] / player["GP"]  # creates new column
        player["AVG_AST"] = player["AVG_AST"].round(0)
        player["AVG_MIN"] = player["MIN"] / player["GP"]  # creates new column
        player["AVG_MIN"] = player["AVG_MIN"].round(0)
        player = player[
            [
                "SEASON_ID",
                "TEAM_ABBREVIATION",
                "AVG_PTS",
                "AVG_REB",
                "AVG_AST",
                "AVG_MIN",
                "PTS",
                "REB",
                "AST",
                "MIN",
            ]
        ]  # narrows data frame to only needed data points
        return player
    elif id[0] == "team":
        team = franchisehistory.FranchiseHistory()  # draws all teams' data
        team = team.get_data_frames()[0]  # generates pandas data frame
        team = team.loc[(team["TEAM_ID"] == id[-1])]  # selects specific team
        team = team.iloc[0]  # narrows the df to the first iteration of the team
        team = team[
            [
                "TEAM_CITY",
                "TEAM_NAME",
                "GAMES",
                "WINS",
                "LOSSES",
                "WIN_PCT",
                "PO_APPEARANCES",
                "CONF_TITLES",
                "LEAGUE_TITLES",
                "START_YEAR",
            ]
        ]  # narrows data frame to only needed data points
        return team
    else:
        return None


def years_in_league(years):
    """
    Calculates the year of the player's first nba season
    """
    current_year = datetime.datetime.now().year  # current year
    return current_year - (years - 1)


def generate_report(name, id, data):
    """
    Generates a visual report of compiled statistics
    """
    classifier = id[0]  # classifies either team or player variables
    years = len(data)  # calculates how many years the player has been in the nba
    first_year = years_in_league(years)
    if classifier == "player":
        print(
            f"\n{name} has played in the NBA for {years} years.\n\nStarting back in the {first_year}-{first_year + 1} NBA season, {name} played for {data['TEAM_ABBREVIATION'][0]}, where he averaged {data['AVG_PTS'][0]} points per game.\n\nToday, {name} plays for {data['TEAM_ABBREVIATION'][years - 1]} where he averages {data['AVG_PTS'][years - 1]} points per game.\n\n{name} has {data['PTS'].sum()} total career points and has played for {data['TEAM_ABBREVIATION'].nunique()} different teams.\n"
        )
    elif classifier == "team":
        print(
            f"\nThe {name} franchise have won {data['LEAGUE_TITLES']} NBA championships since {data['START_YEAR']}.\n\nThe {name} have {data['WINS']} total wins and {data['LOSSES']} losses and have made it to the NBA playoffs {data['PO_APPEARANCES']} times.\n"
        )
    else:
        return None


def live_games():
    """
    Prints today's NBA scheduled games.
    """
    board = scoreboard.ScoreBoard()
    print(f"\nToday's NBA Schedule: {board.score_board_date}")
    for game in board.games.get_dict():
        gametime = parser.parse(game["gameTimeUTC"]).astimezone(tz=None)
        print(
            f"{game['awayTeam']['teamName']} vs. {game['homeTeam']['teamName']} @ {gametime}"
        )


def main():
    user_input = input("Enter a team or player: ")
    subject = identify_subject(user_input)
    data = fetch_data(subject)
    generate_report(user_input, subject, data)
    live_games()


if __name__ == "__main__":
    main()
