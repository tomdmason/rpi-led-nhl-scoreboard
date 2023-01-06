from api.nhlService import NhlService
from api.mlbService import MlbService
import random
import time

def fetchGameData ():
    nhlService = NhlService()
    mlbService = MlbService()

    services = [nhlService, mlbService]

    networkError = False
    games = []

    # Try to get team and game data. Max of 100 attempts before it gives up.
    for i in range(100):
        try:
            for service in services:
                games.append(service.getGameData())
            
            random.shuffle(games)
            networkError = False
            break

            # In the event that the NHL API cannot be reached, set the bottom right LED to red.
            # TODO: Make this more robust for specific fail cases.
        except Exception as e:
            print(e)
            networkError = True
            time.sleep(1)
    
    if networkError == True:
        raise Exception("Unable to fetch game data")

    return games
        
def fetchMlbGame(gameId):
    mlbService = MlbService()
    return mlbService.getGameDetails(gameId)

# fetchGameData()