from PIL import Image, ImageDraw, ImageFont
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from datetime import datetime
import time
from util import imageUtil, timeUtil
from api.gameData import fetchGameData, fetchMlbGame
from renderers.nhlGameRenderer import NhlGameRenderer
from renderers.mlbGameRenderer import MlbGameRenderer


def buildNoGamesToday():
    """Adds all aspects of the no games today screen to the image object."""

    # Add the NHL logo to the image.
    nhlLogo = Image.open("assets/images/NHL_Logo_Simplified.png")
    nhlLogo = imageUtil.cropImage(nhlLogo)
    nhlLogo.thumbnail((25,15))
    image.paste(nhlLogo, (1, 1))

    mlbLogo = Image.open("assets/images/MLB_Logo.png")
    mlbLogo = imageUtil.cropImage(mlbLogo)
    mlbLogo.thumbnail((20,30))
    image.paste(mlbLogo, (1, 20))

    # Add "No Games Today" to the image.
    draw.text((32,0), "No", font=fontMedReg, fill=fillWhite)
    draw.text((32,10), "Games", font=fontMedReg, fill=fillWhite)
    draw.text((32,20), "Today", font=fontMedReg, fill=fillWhite)

def buildLoading():
    """Adds all aspects of the loading screen to the image object."""

    # Add the NHL logo to the image.
    nhlLogo = Image.open("assets/images/NHL_Logo_Simplified.png")
    nhlLogo = imageUtil.cropImage(nhlLogo)
    nhlLogo.thumbnail((40,30))
    image.paste(nhlLogo, (1, 1))

    mlbLogo = Image.open("assets/images/MLB_Logo.png")
    mlbLogo = imageUtil.cropImage(mlbLogo)
    mlbLogo.thumbnail((30,60))
    image.paste(mlbLogo, (30, 8))

def buildError(msg):
    """
        Error screen
    """
    draw.text((32,0), "Error", font=fontMedReg, fill=fillWhite)
    draw.text((32,10), msg, font=fontMedReg, fill=fillWhite)

def fadeOut(maxBrightness, fadeStep):
     # Fade down to black.
    for brightness in range(maxBrightness,0,-fadeStep):
        matrix.brightness = brightness
        matrix.SetImage(image)
        time.sleep(.025)

    # Make the screen totally blank between fades.
    draw.rectangle(((0,0),(63,31)), fill=fillBlack) 
    matrix.SetImage(image)

def fadeIn(maxBrightness, fadeStep):
    # Fade up to the image.
    for brightness in range(0,maxBrightness,fadeStep):
        matrix.brightness = brightness
        matrix.SetImage(image)
        time.sleep(.025)


def runScoreboard():
    """Runs the scoreboard geting scores and other game data and cycles through them in an infinite loop."""

    # Initial calculation and setting of the max brightness.
    maxBrightness, fadeStep = timeUtil.getMaxBrightness(int(datetime.now().strftime("%H")))
    matrix.brightness = maxBrightness

    # Build the loading screen.
    buildLoading()
    matrix.SetImage(image) # Set the matrix to the image.

    try:
        games = fetchGameData()
    except Exception as e:
        fadeOut(maxBrightness, fadeStep)
        buildError(e)
        fadeIn(maxBrightness, fadeStep)

    time.sleep(1)


    fadeOut(maxBrightness, fadeStep)

    nhlRenderer = NhlGameRenderer(matrix, image, draw)
    mlbRenderer = MlbGameRenderer(matrix, image, draw)

    while True:

        # Adjusting cycle time for single game situation.
        if len(games) == 1:
            cycleTime = 10
        else:
            cycleTime = 3.5

        # If there's games today.
        if games:
            for game in games:
                if game['League'] == "nhl":
                    nhlRenderer.render(game)
                if game['League'] == "mlb":
                    details = fetchMlbGame(game['Game ID'])
                    mlbRenderer.render(details)

                fadeIn(maxBrightness, fadeStep)

                # Hold the screen before fading.
                time.sleep(cycleTime)

                fadeOut(maxBrightness, fadeStep)

        # If there's no games, build the no games today sceen, then wait 10 minutes before checking again.
        else:
            buildNoGamesToday()
            matrix.brightness = maxBrightness
            matrix.SetImage(image)
            time.sleep(600)
            draw.rectangle(((0,0),(63,31)), fill=fillBlack)
        
        # Refresh the game data.
        # Record the data of the last cycle in gamesOld to check for goals.
        try:
            games = fetchGameData()
        except Exception as e:
            fadeOut(maxBrightness, fadeStep)
            buildError(e)
            fadeIn(maxBrightness, fadeStep)

if __name__ == "__main__":

    # This creates the options, matrix, and image objects, as well as some globals that will be needed throughout the code.
    # Note a huge fan of the ammount of globals, but they work fine in a small scope project like this.

    # Configure options for the matrix
    options = RGBMatrixOptions()
    options.rows = 32
    options.cols = 64
    options.chain_length = 1
    options.parallel = 1
    options.gpio_slowdown= 2
    options.hardware_mapping = 'adafruit-hat'

    # Define a matrix object from the options.
    matrix = RGBMatrix(options = options)

    # Define an image object that will be printed to the matrix.
    image = Image.new("RGB", (64, 32))

    # Define a draw object. This will be used to draw shapes and text to the image.
    draw = ImageDraw.Draw(image)

    # Declare fonts that are used throughout.
    fontSmallReg = ImageFont.load("assets/fonts/PIL/Tamzen5x9r.pil")
    fontSmallBold = ImageFont.load("assets/fonts/PIL/Tamzen5x9b.pil")
    fontMedReg = ImageFont.load("assets/fonts/PIL/Tamzen6x12r.pil")
    fontMedBold = ImageFont.load("assets/fonts/PIL/Tamzen6x12b.pil")
    fontLargeReg = ImageFont.load("assets/fonts/PIL/Tamzen8x15r.pil")
    fontLargeBold = ImageFont.load("assets/fonts/PIL/Tamzen8x15b.pil")

    # Declare text colours that are needed.
    fillWhite = 255,255,255,255
    fillBlack = 0,0,0,255
    fillRed = 255,50,50,255

    # Define the first col that can be used for center text.
    # i.e. the first col you can use without worry of logo overlap.
    firstMiddleCol = 21

    # Define the number of seconds to sit on each game.
    cycleTime = 33.5

    # Run the scoreboard.
    runScoreboard()
