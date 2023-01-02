from PIL import Image, ImageDraw, ImageFont
from util import imageUtil
import math

class CommonRenderer: 

    def __init__(self, matrix, image, draw) -> None:
            super().__init__()
            self.matrix = matrix
            self.image = image
            self.draw = draw
            # Declare fonts that are used throughout.
            self.fontSmallReg = ImageFont.load("assets/fonts/PIL/Tamzen5x9r.pil")
            self.fontSmallBold = ImageFont.load("assets/fonts/PIL/Tamzen5x9b.pil")
            self.fontMedReg = ImageFont.load("assets/fonts/PIL/Tamzen6x12r.pil")
            self.fontMedBold = ImageFont.load("assets/fonts/PIL/Tamzen6x12b.pil")
            self.fontLargeReg = ImageFont.load("assets/fonts/PIL/Tamzen8x15r.pil")
            self.fontLargeBold = ImageFont.load("assets/fonts/PIL/Tamzen8x15b.pil")

            # Declare text colours that are needed.
            self.fillWhite = 255,255,255,255
            self.fillBlack = 0,0,0,255
            self.fillRed = 255,50,50,255

            # Define the first col that can be used for center text.
            # i.e. the first col you can use without worry of logo overlap.
            self.firstMiddleCol = 21

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
        awayLogo = imageUtil.resizeImage(awayLogo)
        awayLogo.thumbnail(logoSize)

        # Load, crop, and resize the home team logo.
        homeLogo = Image.open("assets/images/team logos/" + league + "/png/" + homeTeam + ".png")
        homeLogo = imageUtil.cropImage(homeLogo)
        homeLogo = imageUtil.resizeImage(homeLogo)
        homeLogo.thumbnail(logoSize)

        # Add the logos to the image.
        # Logos will be bounded by the text region, and be centered vertically.
        self.image.paste(awayLogo, (2, 8))
        self.image.paste(homeLogo, (42, 8))