from renderers.commonRenderer import CommonRenderer
from PIL import Image, ImageDraw, ImageFont
from util import imageUtil
import math

class MlbGameRenderer(CommonRenderer):
    def __init__(self, matrix, image, draw) -> None:
        super().__init__(matrix, image, draw)

    def render(self, game):

        # If the GameId is the NO_GAME indicator, render no games
        if game['gameId'] == 'NO_GAMES':
            self.buildNoGames()
            return

        # If the game is postponed, build the postponed screen.
        if game['status'] == "Postponed":
            self.buildGamePostponed(game)

        # If the game has yet to begin, build the game not started screen.
        elif game['status'] == "Preview":
            self.buildGameNotStarted(game)

        # If the game is over, build the final score screen.
        elif game['status'] == "Final":
            self.buildGameOver(game)
        
        # Otherwise, the game is in progress. Build the game in progress screen.
        else:
            self.buildGameInProgress(game)

    

    def buildGameNotStarted(self, game):
        """Adds all aspects of the game not started screen to the image object.

        Args:
            game (dict): All information for a specific game.
        """

        # Add the logos of the teams inivolved to the image.
        self.displayLogos(game['league'],game['awayAbbrev'],game['homeAbbrev'])

        self.displayTime(game['dateTime']['time'] + " " + game['dateTime']['ampm'], (self.firstMiddleCol, 0))
        
        self.draw.text((self.firstMiddleCol+1,8), game['awayStartingPitcher'], font=self.fontSmallReg, fill=self.fillWhite)

        self.draw.text((self.firstMiddleCol+3,16), 'vs', font=self.fontSmallReg, fill=self.fillWhite)

        self.draw.text((self.firstMiddleCol+1,24), game['homeStartingPitcher'], font=self.fontSmallReg, fill=self.fillWhite)



    def buildGameInProgress(self, game):
        """Adds all aspects of the game in progress screen to the image object.

        Args:
            game (dict): All information for a specific game.
            gameOld (dict): The same information, but from one cycle ago.
            scoringTeam (string): If the home team, away team, or both, or neither scored.
        """

        # Add the logos of the teams inivolved to the image.
        self.displayLogos(game['league'],game['awayAbbrev'],game['homeAbbrev'])

        if game['inningState'] != "Top":
            self.draw.polygon([(43,17), (45, 17), (44,18)],fill=self.fillWhite, outline=self.fillWhite)
        if game['inningState'] != "Bottom":
            self.draw.polygon([(43,15), (45, 15), (44,14)],fill=self.fillWhite, outline=self.fillWhite)

        self.displayAtBat(game)
        self.displayBaseRunners(game)

        self.draw.text((47, 12), str(game['currentInning']), font=self.fontSmallReg, fill=self.fillWhite)

        # Add the current score to the image. Note if either team scored.
        self.displayScore(game)

    def displayAtBat(self, game):
        balls = game['balls']
        strikes = game['strikes']
        outs = game['outs']

        # Count
        self.draw.text((41, 22), f'{balls}-{strikes}', font=self.fontSmallReg, fill=self.fillWhite)

        fillOne = self.fillWhite if outs > 0 else None
        fillTwo = self.fillWhite if outs > 1 else None

        # Outs
        self.draw.ellipse([(58, 4), (62, 8)], fill=fillOne, outline=self.fillWhite)
        self.draw.ellipse([(58, 10), (62, 14)], fill=fillTwo, outline=self.fillWhite)

    def displayBaseRunners(self, game):
        onFirst = self.fillWhite if game['onFirst'] else None
        onSecond = self.fillWhite if game['onSecond'] else None
        onThird = self.fillWhite if game['onThird'] else None

        self.draw.polygon([(39, 9), (42, 6), (45, 9), (42, 12)], fill=onThird, outline=self.fillWhite)
        self.draw.polygon([(44, 4), (47, 1), (50, 4), (47, 7)], fill=onSecond, outline=self.fillWhite)
        self.draw.polygon([(49, 9), (52, 6), (55, 9), (52, 12)], fill=onFirst, outline=self.fillWhite)
        
        


    def buildGameOver(self, game):
        """Adds all aspects of the game over screen to the image object.

        Args:
            game (dict): All information for a specific game.
            scoringTeam (string): If the home team, away team, or both, or neither scored.
        """

        # Add the logos of the teams involved to the image.
        self.displayLogos(game['league'],game['awayAbbrev'],game['homeAbbrev'])

        # Add "Final" to the image.
        self.draw.text((40, 11), "F", font=self.fontMedReg, fill=self.fillWhite)
        self.draw.text((44, 13), "i", font=self.fontSmallReg, fill=self.fillWhite)
        self.draw.text((49, 13), "n", font=self.fontSmallReg, fill=self.fillWhite)
        self.draw.text((53, 13), "a", font=self.fontSmallReg, fill=self.fillWhite)
        self.draw.text((57, 13), "l", font=self.fontSmallReg, fill=self.fillWhite)

        # Add the current score to the image. Note if either team scored.
        self.displayScore(game)

    def buildNoGames(self):
        mlbLogo = Image.open("assets/images/MLB_Logo.png")
        mlbLogo = imageUtil.cropImage(mlbLogo)
        mlbLogo.thumbnail((32,32))
        self.image.paste(mlbLogo, (16, 4))
        self.draw.text((12, 22), f'No games', font=self.fontSmallReg, fill=self.fillWhite)

    def buildGamePostponed(self, game):
        """Adds all aspects of the postponed screen to the image object.

        Args:
            game (dict): All information for a specific game.
        """
        
        # Add the logos of the teams involved to the image.
        self.displayLogos(game['league'],game['awayAbbrev'],game['homeAbbrev'])

        # Add "PPD" to the image.
        self.draw.text((self.firstMiddleCol+12,10), "PPD", font=self.fontMedReg, fill=self.fillWhite)

    

    def displayScore(self, game):
        """Add the score for both teams to the image object.

        Args:
            awayScore (int): Score of the away team.
            homeScore (int): Score of the home team.
        """

        awayScore = game['awayRuns']
        homeScore = game['homeRuns']

        awayHits = game['awayHits']
        homeHits = game['homeHits']

        fillHome = self.fillWhite if awayScore > homeScore or awayScore == homeScore else self.fillRed
        fillAway = self.fillWhite if awayScore < homeScore or awayScore == homeScore else self.fillRed

        self.draw.text((21,-1), f'R', font=self.fontSmallReg, fill=fillAway)
        self.draw.text((26,-1), f'{awayScore}', font=self.fontSmallReg, fill=fillAway)

        self.draw.text((21,6), f'H', font=self.fontSmallReg, fill=self.fillWhite)
        self.draw.text((26,6), f'{awayHits}', font=self.fontSmallReg, fill=self.fillWhite)
        
        self.draw.text((21,16), f'R', font=self.fontSmallReg, fill=fillHome)
        self.draw.text((26,16), f'{homeScore}', font=self.fontSmallReg, fill=fillHome)

        self.draw.text((21,23), f'H', font=self.fontSmallReg, fill=self.fillWhite)
        self.draw.text((26,23), f'{homeHits}', font=self.fontSmallReg, fill=self.fillWhite)


        