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

            self.fontMonteBold = ImageFont.load("assets/fonts/PIL/MonteCarloBold.pil")
            self.fontMonteReg = ImageFont.load("assets/fonts/PIL/MonteCarloMedium.pil")

            self.fontXsReg = ImageFont.load("assets/fonts/PIL/4x6.pil")


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
        logoSize = (16,16)

        # Load, crop, and resize the away team logo.
        awayLogo = Image.open("assets/images/team logos/" + league + "/png/" + awayTeam + ".png")
        awayLogo = imageUtil.cropImage(awayLogo)
        awayLogo.thumbnail(logoSize)

        # Load, crop, and resize the home team logo.
        homeLogo = Image.open("assets/images/team logos/" + league + "/png/" + homeTeam + ".png")
        homeLogo = imageUtil.cropImage(homeLogo)
        homeLogo.thumbnail(logoSize)

        awayLogoWidth, awayLogoHeight = awayLogo.size
        homeLogoWidth, homeLogoHeight = homeLogo.size

        # Add the logos to the image.
        # Logos will be bounded by the text region, and be centered vertically.
        self.image.paste(awayLogo, ((10 - math.floor(awayLogoWidth / 2)), 8 - math.ceil(awayLogoHeight / 2)))
        self.image.paste(homeLogo, ((10 - math.floor(homeLogoWidth / 2)), 24 - math.floor(homeLogoHeight / 2)))