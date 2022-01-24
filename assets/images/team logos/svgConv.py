import os
from os import path
from cairosvg import svg2png

def main():
    # Converts all .svg files in the source directory to .png. Saves to the destination directory.
    # Set source and destination as needed.
    
    # source = '/home/pi/nhl_scoreboard/Assets/Images/Team Logos/SVG/'
    # destination = '/home/pi/nhl_scoreboard/Assets/Images/Team Logos/PNG/'

    source = '/home/pi/dev/rpi-led-nhl-scoreboard/assets/images/team logos/mlb/svg/'
    destination = '/home/pi/dev/rpi-led-nhl-scoreboard/assets/images/team logos/mlb/png/'

    for filename in os.listdir(source):
        print(filename)
        if filename.endswith('.svg'):
            svg2png(url=source+filename, write_to=destination+filename[0:3]+".png")

if __name__ == '__main__':
    main()