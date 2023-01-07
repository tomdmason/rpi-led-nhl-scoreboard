import requests
from .api import LeagueApiInterface
from datetime import datetime
from util import timeUtil

class NhlService(LeagueApiInterface):
    def getTeamData(self):
        """Get team names and abreviations from the NHL API, return information as a list of dictionaries.

        Returns:
            teams (list of dictionaries): Each dict contains the longform name and abbreviation of a single NHL team.
        """
        # Call the NHL Teams API. Store as a JSON object.
        teamsResponse = requests.get(url="https://statsapi.web.nhl.com/api/v1/teams")
        teamsJson = teamsResponse.json()

        # Decalare an empty list to hold the team dicts.
        teams = []

        # For each team, build a dict recording it's name and abbreviation. Append this to the end of the teams list.
        for team in teamsJson['teams']:
            teamDict = {
                    'Team Name': team['name'],
                    'Team Abbreviation': team['abbreviation']
            }
            # Append dict to the end of the teams list.
            teams.append(teamDict)
        
        return teams

    def getGameData(self):
        """Get game data for all of todays games from the NHL API, returns games as a list of dictionaries.

        Args:
            teams (list of dictionaries): Team names and abberivations. Needed as the game API doen't return team abbreviations.

        Returns:
            games (list of dictionaries): All game info needed to display on scoreboard. Teams, scores, start times, game clock, etc.
        """

        teams = self.getTeamData()

        # Call the NHL API for today's game info. Save the rsult as a JSON object.
        gamesResponse = requests.get(url="https://statsapi.web.nhl.com/api/v1/schedule?expand=schedule.linescore&date=" + datetime.today().strftime('%Y-%m-%d'))
        gamesJson = gamesResponse.json()

        # Decalare an empty list to hold the games dicts.
        games = []
        
        # For each game, build a dict recording it's information. Append this to the end of the teams list.
        if gamesJson['dates']: # If games today.
            for game in gamesJson['dates'][0]['games']:

                # Prep the period data for consistancy. This data doesn't exist in the API responce until game begins.
                if 'linescore' in game and 'currentPeriodOrdinal' in game['linescore']:
                    perName = game['linescore']['currentPeriodOrdinal']
                    perTimeRem = game['linescore']['currentPeriodTimeRemaining']
                else:
                    perName = "Not Started"
                    perTimeRem = "Not Started"

                # Prep the dict data.
                gameDict = {
                    'Game ID': game['gamePk'],
                    'Home Team': game['teams']['home']['team']['name'],
                    # Since the schedule API doesn't have team abreviatiosn, we'll have to get that from the team dict.
                    'Home Abbreviation': [t['Team Abbreviation'] for t in teams if t['Team Name'] == game['teams']['home']['team']['name']][0],
                    'Away Team': game['teams']['away']['team']['name'],
                    # Since the schedule API doesn't have team abreviatiosn, we'll have to get that from the team dict.
                    'Away Abbreviation': [t['Team Abbreviation'] for t in teams if t['Team Name'] == game['teams']['away']['team']['name']][0],
                    'Home Score': game['teams']['home']['score'],
                    'Away Score': game['teams']['away']['score'],
                    'Start Time UTC':  datetime.strptime(game['gameDate'], '%Y-%m-%dT%H:%M:%SZ'), # Extracts the startime from what's given by the API.
                    'Start Time Local': timeUtil.utcToLocal(datetime.strptime(game['gameDate'], '%Y-%m-%dT%H:%M:%SZ')), # Converts the UTC start time to the RPi's local timezone.
                    'Status': game['status']['abstractGameState'],
                    'Detailed Status': game['status']['detailedState'],
                    'Period Number': game['linescore']['currentPeriod'],
                    'Period Name': perName,
                    'Period Time Remaining': perTimeRem,
                    'league': 'nhl'
                }

                # Append the dict to the games list.
                games.append(gameDict)

                # Sort list by Game ID. Ensures order doesn't cahnge as games end.
                games.sort(key=lambda x:x['Game ID'])

            if len(games) == 0:
                games.append({
                    'gameId': 'NO_GAMES',
                    'league': "nhl"
                })
        return games
