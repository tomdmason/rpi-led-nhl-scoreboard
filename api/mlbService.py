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

    def getGameData(self):
        """Get game data for all of todays games from the NHL API, returns games as a list of dictionaries.

        Args:
            teams (list of dictionaries): Team names and abberivations. Needed as the game API doen't return team abbreviations.

        Returns:
            games (list of dictionaries): All game info needed to display on scoreboard. Teams, scores, start times, game clock, etc.
        """

        

        # Call the NHL API for today's game info. Save the rsult as a JSON object.
        gamesResponse = requests.get(url=self.BASE_URL + self.ENDPOINT_SCHEDULE)
        gamesJson = gamesResponse.json()

        # Decalare an empty list to hold the games dicts.
        games = []

        # For each game, build a dict recording it's information. Append this to the end of the teams list.
        if gamesJson['dates']: # If games today.
            for game in gamesJson['dates'][0]['games']:

                try:
                    # Prep the dict data.
                    gameDict = {
                        'Game ID': game['gamePk'],
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
        return games

    def getGameDetails(self, gameId):
        feed = requests.get(url=f'https://statsapi.mlb.com/api/v1.1/game/{gameId}/feed/live')
        feed = feed.json()

        gameData = feed['gameData']
        teams = gameData['teams']
        linescore = feed['liveData']['linescore']

        first = []
        second = []
        third = []

        if 'first' in linescore['offense']:
            first = linescore['offense']['first']

        if 'second' in linescore['offense']:
            second = linescore['offense']['second']

        if 'third' in linescore['offense']:
            third = linescore['offense']['third']

        try:
            # Prep the dict data.
            return {
                'Game ID': gameId,
                'Home Team': teams['home']['name'],
                'Home Abbreviation': teams['home']['abbreviation'],
                'Away Team': teams['away']['name'],
                'Away Abbreviation': teams['away']['abbreviation'],
                'Home Score': linescore['teams']['home']['runs'],
                'Away Score': linescore['teams']['away']['runs'],
                'Home Hits': linescore['teams']['home']['hits'],
                'Away Hits': linescore['teams']['away']['hits'],
                'Status': gameData['status']['abstractGameState'],
                'Current Inning': linescore['currentInningOrdinal'],
                'Inning State': linescore['inningState'],
                'Balls': linescore['balls'],
                'Strikes': linescore['strikes'],
                'Outs': linescore['outs'],
                'At Bat': linescore['offense']['batter'],
                'On First': first,
                'On Second': second,
                'On Third': third,
                'League': "mlb"
            }                    
        except Exception as e:
            print("Caught")
            print(e)
            print(gameId)

