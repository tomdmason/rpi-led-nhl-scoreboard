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
        if game['Status'] == "Final":
            self.buildGameOver(game)
        
        # Otherwise, the game is in progress. Build the game in progress screen.
        else:
            self.buildGameInProgress(game)

    def displayLogos(self, league, awayTeam, homeTeam):
        """Adds the logos of the home and away teams to the image object, making sure to not overlap text and center logos.

        Args:
            awayTeam (string): Abbreviation of the away team.
            homeTeam (string): Abbreviation of the home team.
        """

        # Difine the max width and height that a logo can be.
        logoSize = (20,20)

        # Load, crop, and resize the away team logo.
        awayLogo = Image.open("assets/images/team logos/" + league + "/png/" + awayTeam + ".png")
        awayLogo = imageUtil.cropImage(awayLogo)
        awayLogo.crop((16, 16, 24, 24))

        # Load, crop, and resize the home team logo.
        homeLogo = Image.open("assets/images/team logos/" + league + "/png/" + homeTeam + ".png")
        homeLogo = imageUtil.cropImage(homeLogo)
        homeLogo.crop((16, 16, 24, 24))

        # Add the logos to the image.
        # Logos will be bounded by the text region, and be centered vertically.
        self.image.paste(awayLogo, (2, 2))
        self.image.paste(homeLogo, (2, 22))

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
        self.displayLogos(game['League'],game['Away Abbreviation'],game['Home Abbreviation'])

        # Add the period to the image.
        self.displayPeriod(game['Period Number'], game['Period Name'], game['Period Time Remaining'])

        # Add the current score to the image. Note if either team scored.
        self.displayScore(game['Away Score'], game['Home Score'])

    def buildGameOver(self, game):
        """Adds all aspects of the game over screen to the image object.

        Args:
            game (dict): All information for a specific game.
            scoringTeam (string): If the home team, away team, or both, or neither scored.
        """

        # Add the logos of the teams involved to the image.
        self.displayLogos(game['League'],game['Away Abbreviation'],game['Home Abbreviation'])

        # Add "Final" to the image.
        self.draw.text((self.firstMiddleCol+1,0), "F", font=self.fontMedReg, fill=self.fillWhite)
        self.draw.text((self.firstMiddleCol+5,2), "i", font=self.fontSmallReg, fill=self.fillWhite)
        self.draw.text((self.firstMiddleCol+9,2), "n", font=self.fontSmallReg, fill=self.fillWhite)
        self.draw.text((self.firstMiddleCol+14,2), "a", font=self.fontSmallReg, fill=self.fillWhite)
        self.draw.text((self.firstMiddleCol+17,2), "l", font=self.fontSmallReg, fill=self.fillWhite)

        # Add the current score to the image.
        self.displayScore(game['Away Score'],game['Home Score'])

    def buildGamePostponed(self, game):
        """Adds all aspects of the postponed screen to the image object.

        Args:
            game (dict): All information for a specific game.
        """
        
        # Add the logos of the teams involved to the image.
        self.displayLogos(game['League'],game['Away Abbreviation'],game['Home Abbreviation'])

        # Add "PPD" to the image.
        self.draw.text((self.firstMiddleCol+2,0), "PPD", font=self.fontMedReg, fill=self.fillWhite)

    

    def displayScore(self, awayScore, homeScore):
        """Add the score for both teams to the image object.

        Args:
            awayScore (int): Score of the away team.
            homeScore (int): Score of the home team.
        """

        # Add the hypen to the image.
        self.draw.text((self.firstMiddleCol+9,20), "-", font=self.fontSmallBold, fill=self.fillWhite)

        self.draw.text((self.firstMiddleCol+1,17), str(awayScore), font=self.fontLargeBold, fill=self.fillWhite)
        self.draw.text((self.firstMiddleCol+13,17), str(homeScore), font=self.fontLargeBold, fill=(self.fillWhite))