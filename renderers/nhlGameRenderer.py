from renderers.commonRenderer import CommonRenderer
from PIL import Image, ImageDraw, ImageFont
from util import imageUtil

class NhlGameRenderer(CommonRenderer):
    def __init__(self, matrix, image, draw) -> None:
        super().__init__(matrix, image, draw)

    def render(self, game):

        # If the GameId is the NO_GAME indicator, render no games
        if game['gameId'] == 'NO_GAMES':
            self.buildNoGames()
            return

        # If the game is postponed, build the postponed screen.
        if game['detailedStatus'] == "Postponed":
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

    def buildNoGames(self):
        logo = Image.open("assets/images/NHL_Logo_Simplified.png")
        logo = imageUtil.cropImage(logo)
        logo.thumbnail((22, 22))
        self.image.paste(logo, (22, 2))
        self.draw.text((12, 22), f'No games', font=self.fontSmallReg, fill=self.fillWhite)

    def buildGameNotStarted(self, game):
        """Adds all aspects of the game not started screen to the image object.

        Args:
            game (dict): All information for a specific game.
        """

        # Add the logos of the teams inivolved to the image.
        self.displayLogos(game['league'],game['awayAbbreviation'],game['homeAbbreviation'])

        # Extract the start time in 12 hour format.
        time = game['startTimeLocal']
        time = time.time().strftime('%-I:%M %p')
        time = str(time) # Cast to a string for easier parsing.

        self.displayTime(time, (self.firstMiddleCol+1, 12))
        

    def buildGameInProgress(self, game):
        """Adds all aspects of the game in progress screen to the image object.

        Args:
            game (dict): All information for a specific game.
            gameOld (dict): The same information, but from one cycle ago.
            scoringTeam (string): If the home team, away team, or both, or neither scored.
        """

        # Add the logos of the teams inivolved to the image.
        self.displayLogos(game['league'],game['awayAbbreviation'],game['homeAbbreviation'])

        # Add the period to the image.
        self.displayPeriod(game['periodNumber'], game['periodName'], game['periodTimeRemaining'])

        # Add the current score to the image. Note if either team scored.
        self.displayScore(game['awayScore'], game['homeScore'])

    def buildGameOver(self, game):
        """Adds all aspects of the game over screen to the image object.

        Args:
            game (dict): All information for a specific game.
            scoringTeam (string): If the home team, away team, or both, or neither scored.
        """

        # Add the logos of the teams involved to the image.
        self.displayLogos(game['league'],game['awayAbbreviation'],game['homeAbbreviation'])

        # Add "Final" to the image.
        self.draw.text((self.firstMiddleCol+1,0), "F", font=self.fontMedReg, fill=self.fillWhite)
        self.draw.text((self.firstMiddleCol+5,2), "i", font=self.fontSmallReg, fill=self.fillWhite)
        self.draw.text((self.firstMiddleCol+9,2), "n", font=self.fontSmallReg, fill=self.fillWhite)
        self.draw.text((self.firstMiddleCol+14,2), "a", font=self.fontSmallReg, fill=self.fillWhite)
        self.draw.text((self.firstMiddleCol+17,2), "l", font=self.fontSmallReg, fill=self.fillWhite)

        # Check if the game ended in overtime or a shootout.
        # If so, add that to the image.
        if game['periodName'] == "OT" or game['periodName'] == "SO":
            self.draw.text((self.firstMiddleCol+6,9), game['periodName'], font=self.fontMedReg, fill=self.fillWhite)
        elif game['periodNumber'] > 4: # If the game ended in 2OT or later.
            self.draw.text((self.firstMiddleCol+3,9), game["periodName"], font=self.fontMedReg, fill=self.fillWhite)

        # Add the current score to the image.
        self.displayScore(game['awayScore'],game['homeScore'])

    def buildGamePostponed(self, game):
        """Adds all aspects of the postponed screen to the image object.

        Args:
            game (dict): All information for a specific game.
        """
        
        # Add the logos of the teams involved to the image.
        self.displayLogos(game['league'],game['awayAbbreviation'],game['homeAbbreviation'])

        # Add "PPD" to the image.
        self.draw.text((self.firstMiddleCol+2,0), "PPD", font=self.fontMedReg, fill=self.fillWhite)

    def displayPeriod(self, periodNumber, periodName, timeRemaining):
        """Adds the current period to the image object.

        Args:
            periodNumber (int): [description]
            periodName (string): [description]
            timeRemaining (string): [description]
        """

        # If the first period, add "1st" to the image.
        if periodNumber == 1:
            self.draw.text((self.firstMiddleCol+5,2), "1", font=self.fontMedReg, fill=self.fillWhite)
            self.draw.text((self.firstMiddleCol+9,2), "s", font=self.fontSmallReg, fill=self.fillWhite)
            self.draw.text((self.firstMiddleCol+13,2), "t", font=self.fontSmallReg, fill=self.fillWhite)

        # If the second period, add "2nd" to the image.
        elif periodNumber == 2:
            self.draw.text((self.firstMiddleCol+4,2), "2", font=self.fontMedReg, fill=self.fillWhite)
            self.draw.text((self.firstMiddleCol+10,2), "n", font=self.fontSmallReg, fill=self.fillWhite)
            self.draw.text((self.firstMiddleCol+14,2), "d", font=self.fontSmallReg, fill=self.fillWhite)

        # If the third period, add "3rd" to the image.
        elif periodNumber == 3:
            self.draw.text((self.firstMiddleCol+4,2), "3", font=self.fontMedReg, fill=self.fillWhite)
            self.draw.text((self.firstMiddleCol+10,2), "r", font=self.fontSmallReg, fill=self.fillWhite)
            self.draw.text((self.firstMiddleCol+14,2), "d", font=self.fontSmallReg, fill=self.fillWhite)

        # If in overtime/shootout, add that to the image.
        elif periodName == "OT" or periodName == "SO":
            self.draw.text((self.firstMiddleCol+5,2), periodName, font=self.fontSmallReg, fill=self.fillWhite)

        # Otherwise, we're in 2OT or later. Add that to the image.
        else:
            self.draw.text((self.firstMiddleCol+3,2), periodName, font=self.fontSmallReg, fill=self.fillWhite)

        self.displayTime('0:56', (self.firstMiddleCol+3, 22)) # Adds the time remaining in the period to the image.

        # If not in the SO, and the period not over, add the time remaining in the period to the image.
        if periodName != "SO":
            if timeRemaining != "END":
                print('Time')
                print(timeRemaining)
                self.displayTime(timeRemaining, (self.firstMiddleCol+3, 12)) # Adds the time remaining in the period to the image.

            # If not in the SO and the time remaining is "END", then we know that we're in intermission. Don't add time remaininig to the image.
            else:
                self.draw.text((self.firstMiddleCol+2,12), "INT", font=self.fontSmallReg, fill=self.fillWhite)
        
    def displayScore(self, awayScore, homeScore):
        """Add the score for both teams to the image object.

        Args:
            awayScore (int): Score of the away team.
            homeScore (int): Score of the home team.
        """

        fillHome = self.fillWhite if awayScore > homeScore or awayScore == homeScore else self.fillRed
        fillAway = self.fillWhite if awayScore < homeScore or awayScore == homeScore else self.fillRed

        self.draw.text((50,-1), f'{awayScore}', font=self.fontLargeBold, fill=fillAway)
        
        self.draw.text((50,16), f'{homeScore}', font=self.fontLargeBold, fill=fillHome)
