from renderers.commonRenderer import CommonRenderer
from PIL import Image, ImageDraw, ImageFont
from util import imageUtil
import math

class MlbGameRenderer(CommonRenderer):
    def __init__(self, matrix, image, draw) -> None:
        super().__init__(matrix, image, draw)

    def render(self, game):
        # If the game is postponed, build the postponed screen.
        # if game['Status'] == "Postponed":
            # self.buildGamePostponed(game)

        # If the game has yet to begin, build the game not started screen.
        # elif game['Status'] == "Preview":
            # self.buildGameNotStarted(game)

        # If the game is over, build the final score screen.
        if game['status'] == "Final":
            self.buildGameOver(game)
        
        # Otherwise, the game is in progress. Build the game in progress screen.
        else:
            self.buildGameInProgress(game)

    

    def buildGameNotStarted(self, game):
        """Adds all aspects of the game not started screen to the image object.

        Args:
            game (dict): All information for a specific game.
        """

        print('Not implemented')

    def buildGameInProgress(self, game):
        """Adds all aspects of the game in progress screen to the image object.

        Args:
            game (dict): All information for a specific game.
            gameOld (dict): The same information, but from one cycle ago.
            scoringTeam (string): If the home team, away team, or both, or neither scored.
        """

        # Add the logos of the teams inivolved to the image.
        self.displayLogos(game['league'],game['awayAbbrev'],game['homeAbbrev'])

        print(game['inningState'])
        if game['inningState'] == "Bottom":
            self.draw.polygon([(20,13), (24, 13), (22,15)],fill=(0, 192, 192), outline=self.fillWhite)
        else:
            self.draw.polygon([(20,15), (24, 15), (22,13)],fill=(0, 192, 192), outline=self.fillWhite)

        # Add the current score to the image. Note if either team scored.
        self.displayScore(game)

    def buildGameOver(self, game):
        """Adds all aspects of the game over screen to the image object.

        Args:
            game (dict): All information for a specific game.
            scoringTeam (string): If the home team, away team, or both, or neither scored.
        """

        # Add the logos of the teams involved to the image.
        self.displayLogos(game['league'],game['awayAbbrev'],game['homeAbbrev'])

        # Add "Final" to the image.
        self.draw.text((19, 11), "F", font=self.fontMedReg, fill=self.fillWhite)
        self.draw.text((23, 13), "i", font=self.fontSmallReg, fill=self.fillWhite)
        self.draw.text((28, 13), "n", font=self.fontSmallReg, fill=self.fillWhite)
        self.draw.text((32, 13), "a", font=self.fontSmallReg, fill=self.fillWhite)
        self.draw.text((36, 13), "l", font=self.fontSmallReg, fill=self.fillWhite)

        # Add the current score to the image. Note if either team scored.
        self.displayScore(game)

        # Add the current score to the image.
        # self.displayScore(game['Away Score'],game['Home Score'])

    def buildGamePostponed(self, game):
        """Adds all aspects of the postponed screen to the image object.

        Args:
            game (dict): All information for a specific game.
        """
        
        # Add the logos of the teams involved to the image.
        self.displayLogos(game['league'],game['awayAbbrev'],game['homeAbbrev'])

        # Add "PPD" to the image.
        self.draw.text((self.firstMiddleCol+2,0), "PPD", font=self.fontMedReg, fill=self.fillWhite)

    

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

        awayErrors = game['awayErrors']
        homeErrors = game['homeErrors']

        fillHome = self.fillWhite if awayScore > homeScore else self.fillRed
        fillAway = self.fillWhite if awayScore < homeScore else self.fillRed

        # Add the hypen to the image.
        self.draw.text((21,2), f'R{awayScore}', font=self.fontSmallReg, fill=fillAway)
        self.draw.text((21,21), f'R{homeScore}', font=self.fontSmallReg, fill=fillHome)

        self.draw.text((31,2), f'H{awayHits}', font=self.fontSmallReg, fill=self.fillWhite)
        self.draw.text((31,21), f'H{homeHits}', font=self.fontSmallReg, fill=self.fillWhite)

        self.draw.text((41,2), f'E{awayErrors}', font=self.fontSmallReg, fill=self.fillWhite)
        self.draw.text((41,21), f'E{homeErrors}', font=self.fontSmallReg, fill=self.fillWhite)