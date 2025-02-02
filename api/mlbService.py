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
        self.ENDPOINT_SCHEDULE = "schedule?sportId=1" #&date=07/10/2022"

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
                        'gameId': game['gamePk'],
                        'league': "mlb"
                    }                    
                except Exception as e:
                    print("Caught")
                    print(e)
                    print(game)

                # Append the dict to the games list.
                games.append(gameDict)

                # Sort list by Game ID. Ensures order doesn't cahnge as games end.
                games.sort(key=lambda x:x['gameId'])
               
        if len(games) == 0:
            print('No Games today')
            games.append({
                'gameId': 'NO_GAMES',
                'league': "mlb"
            })
        return games

    def getGameDetails(self, gameId):

        if gameId == 'NO_GAMES':
            return {'gameId': 'NO_GAMES'}

        feed = requests.get(url=f'https://statsapi.mlb.com/api/v1.1/game/{gameId}/feed/live')
        feed = feed.json()

        try:
            gameData = feed['gameData']
            teams = gameData['teams']
            linescore = feed['liveData']['linescore']
            boxscore = feed['liveData']['boxscore']

            first = []
            second = []
            third = []

            if 'first' in linescore['offense']:
                first = linescore['offense']['first']

            if 'second' in linescore['offense']:
                second = linescore['offense']['second']

            if 'third' in linescore['offense']:
                third = linescore['offense']['third']

            if 'away' in gameData['probablePitchers']:
                awayStartingPitcher = gameData['probablePitchers']['away']['id']
                awayStartingPitcher = gameData['players'][f'ID{awayStartingPitcher}']['lastName']
            else:
                awayStartingPitcher = 'TBD'

            if 'home' in gameData['probablePitchers']:
                homeStartingPitcher = gameData['probablePitchers']['home']['id']
                homeStartingPitcher = gameData['players'][f'ID{homeStartingPitcher}']['lastName']
            else:
                homeStartingPitcher = 'TBD'

            # Prep the dict data.
            return {
                'gameId': gameId,
                'homeTeam': teams['home']['name'],
                'homeAbbrev': teams['home']['abbreviation'],
                'awayTeam': teams['away']['name'],
                'awayAbbrev': teams['away']['abbreviation'],
                'homeRuns': linescore['teams']['home']['runs'],
                'awayRuns': linescore['teams']['away']['runs'],
                'homeHits': linescore['teams']['home']['hits'],
                'awayHits': linescore['teams']['away']['hits'],
                'homeErrors': boxscore['teams']['home']['teamStats']['fielding']['errors'],
                'awayErrors': boxscore['teams']['away']['teamStats']['fielding']['errors'],
                'status': gameData['status']['abstractGameState'],
                'currentInning':  linescore['currentInning'],
                'inningState': linescore['inningState'],
                'balls': linescore['balls'],
                'strikes': linescore['strikes'],
                'outs': linescore['outs'],
                'atBat': linescore['offense']['batter'],
                'onFirst': first,
                'onSecond': second,
                'onThird': third,
                'dateTime': gameData['datetime'],
                'homeStartingPitcher': homeStartingPitcher,
                'awayStartingPitcher': awayStartingPitcher,
                'league': "mlb"
            }                    
        except Exception as e:
            print("Caught")
            print(e)
            print(gameId)

