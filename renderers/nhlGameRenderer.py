from renderers.commonRenderer import CommonRenderer

class NhlGameRenderer(CommonRenderer):
    def __init__(self, matrix, image, draw) -> None:
        super().__init__(matrix, image, draw)

    def render(self, game):
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

    def buildGameNotStarted(self, game):
        """Adds all aspects of the game not started screen to the image object.

        Args:
            game (dict): All information for a specific game.
        """

        # Add the logos of the teams inivolved to the image.
        self.displayLogos(game['league'],game['awayAbbreviation'],game['homeAbbreviation'])

        # Extract the start time in 12 hour format.
        time = game['startTimeLocal']
        time = time.time().strftime('%-I:%M:%p')
        time = str(time) # Cast to a string for easier parsing.
        time = time.split(':')

        spacer = 6 if int(time[0]) > 9 else 1

        self.draw.text((self.firstMiddleCol+1, 12), f'{time[0]}', font=self.fontSmallReg, fill=self.fillWhite)

        self.draw.rectangle(((self.firstMiddleCol+spacer+5,15),(self.firstMiddleCol+spacer+5,15)), fill=self.fillWhite)
        self.draw.rectangle(((self.firstMiddleCol+spacer+5,17),(self.firstMiddleCol+spacer+5,17)), fill=self.fillWhite)

        self.draw.text((self.firstMiddleCol+spacer+7,12), f'{time[1]}', font=self.fontSmallReg, fill=self.fillWhite)
        self.draw.text((self.firstMiddleCol+spacer+18,12), f'{time[2]}', font=self.fontSmallReg, fill=self.fillWhite)
        

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

        # If not in the SO, and the period not over, add the time remaining in the period to the image.
        if periodName != "SO":
            if timeRemaining != "END":
                self.displayTimeRemaing(timeRemaining) # Adds the time remaining in the period to the image.

            # If not in the SO and the time remaining is "END", then we know that we're in intermission. Don't add time remaininig to the image.
            else:
                self.draw.text((self.firstMiddleCol+2,10), "INT", font=self.fontSmallReg, fill=self.fillWhite)

    def displayTimeRemaing(self, timeRemaining):
        """Adds the remaining time in the period to the image. Takes into account diffent widths of time remaining.

        Args:
            timeRemaining (string): The time remaining in the period in "MM:SS" format. For times less than 10 minutes, the minutes should have a leading zero (e.g 09:59).
        """
        # Minutes.
        self.draw.text((self.firstMiddleCol+3,12), timeRemaining[1], font=self.fontSmallReg, fill=self.fillWhite)
        # Colon.
        self.draw.rectangle(((self.firstMiddleCol+8,15),(self.firstMiddleCol+8,15)), fill=self.fillWhite)
        self.draw.rectangle(((self.firstMiddleCol+8,17),(self.firstMiddleCol+8,17)), fill=self.fillWhite)
        # Seconds.
        self.draw.text((self.firstMiddleCol+10,12), timeRemaining[3], font=self.fontSmallReg, fill=self.fillWhite)
        self.draw.text((self.firstMiddleCol+15,12), timeRemaining[4], font=self.fontSmallReg, fill=self.fillWhite)

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
