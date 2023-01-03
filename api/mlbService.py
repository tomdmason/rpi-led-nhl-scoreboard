import requests
from .api import LeagueApiInterface
from datetime import datetime
from util import timeUtil
import json

class MlbService(LeagueApiInterface):
    def __init__(self) -> None:
        super().__init__()
        self.BASE_URL = "https://statsapi.mlb.com/api/v1/"
        self.ENDPOINT_TEAMS = "teams?sportId=1"
        self.ENDPOINT_SCHEDULE = "schedule?sportId=1&date=07/10/2022"

    def getTeamData(self):
        """Get team names and abreviations from the MLB API, return information as a list of dictionaries.

        Returns:
            teams (list of dictionaries): Each dict contains the longform name and abbreviation of a single NHL team.
        """
        
        
        # Call the NHL Teams API. Store as a JSON object.
        try:
            teamsResponse = requests.get(url=self.BASE_URL + self.ENDPOINT_TEAMS)
        except requests.exceptions.HTTPError as errh:
            print ("Http Error:",errh)
        except requests.exceptions.ConnectionError as errc:
            print ("Error Connecting:",errc)
        except requests.exceptions.Timeout as errt:
            print ("Timeout Error:",errt)
        except requests.exceptions.RequestException as err:
            print ("OOps: Something Else",err)
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
        gamesResponse = requests.get(url=self.BASE_URL + self.ENDPOINT_SCHEDULE)
        gamesJson = gamesResponse.json()

        # Decalare an empty list to hold the games dicts.
        games = []

        # For each game, build a dict recording it's information. Append this to the end of the teams list.
        if gamesJson['dates']: # If games today.
            for game in gamesJson['dates'][0]['games']:

                gameId = game['gamePk']
                linescore = requests.get(url=self.BASE_URL + f'game/{gameId}/linescore')
                linescore = linescore.json()

                pbp = requests.get(url=self.BASE_URL + f'game/{gameId}/playByPlay?fields=allPlays,result,description,event,runners,movement')
                pbp = pbp.json()

                try:
                    currentInning = filter(lambda obj: obj['ordinalNum'] == linescore['currentInningOrdinal'], linescore['innings'])
                    inningInfo = list(currentInning)
                    if inningInfo:
                        inningInfo = inningInfo[0]
                    else:
                        inningInfo = []

                    runners = []
                    lastPlay = []
                    if pbp['allPlays']:
                        runners = pbp['allPlays'][-1]['runners']
                        lastPlay = pbp['allPlays'][-1]['result']

                    # Prep the dict data.
                    gameDict = {
                        'Game ID': game['gamePk'],
                        'Home Team': game['teams']['home']['team']['name'],
                        # # Since the schedule API doesn't have team abreviatiosn, we'll have to get that from the team dict.
                        'Home Abbreviation': [t['Team Abbreviation'] for t in teams if t['Team Name'] == game['teams']['home']['team']['name']][0],
                        'Away Team': game['teams']['away']['team']['name'],
                        # Since the schedule API doesn't have team abreviatiosn, we'll have to get that from the team dict.
                        'Away Abbreviation': [t['Team Abbreviation'] for t in teams if t['Team Name'] == game['teams']['away']['team']['name']][0],
                        'Home Score': linescore['teams']['home']['runs'],
                        'Away Score': linescore['teams']['away']['runs'],
                        'Home Hits': linescore['teams']['home']['hits'],
                        'Away Hits': linescore['teams']['away']['hits'],
                        'Status': game['status']['abstractGameState'],
                        'Current Inning': linescore['currentInningOrdinal'],
                        'Current Inning Info': inningInfo,
                        'Inning State': linescore['inningState'],
                        'Balls': linescore['balls'],
                        'Strikes': linescore['strikes'],
                        'Outs': linescore['outs'],
                        'Runners': runners,
                        'Last Play': lastPlay,
                        'League': "mlb"
                    }                    
                except Exception as e:
                    print("Caught")
                    print(e)
                    print(game)

                # Append the dict to the games list.
                games.append(gameDict)

                # Sort list by Game ID. Ensures order doesn't cahnge as games end.
                games.sort(key=lambda x:x['Game ID'])
                # with open('data.json', 'w', encoding='utf-8') as f:
                #         json.dump(games, f, ensure_ascii=False, indent=4)
        return games
