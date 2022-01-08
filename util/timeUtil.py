import math
from datetime import datetime, timezone

def getMaxBrightness(time):
    """ Calculates the maximum brightness and fade step incremements based on the time of day.

    Args:
        time (int): Hour of the day. Can be 0-23.

    Returns:
        maxBrightness (int): The maximum brightness for the LED display.
        fadeStep (int): The increments that the display should fade up and down by.
    """
    
    # If the time is midnight, set the time to 1am to avoid the display fulling turning off.
    if time == 0:
        time = 1

    # Max brihgtness is the time divided by 12 and multiplied by 100. For pm times, the difference between 24 and the time is used.
    # This means that max brightness is at noon, with the lowest from 11pm through 1am (because of the above edge case).
    maxBrightness = math.ceil(100 * time / 12 if time <= 12 else 100 * (24-time)/12)
    
    # If the previous calculation results in a birhgtness less than 15, set brightnes to 15.
    maxBrightness = maxBrightness if maxBrightness >= 15 else 15

    # Fade step divides the maxBrightness into 15 segments. Floor since you can't have fractional brightness.
    fadeStep = math.ceil(maxBrightness/15)

    return maxBrightness, fadeStep

def utcToLocal(utc_dt):
    """Returns a time object converted to the local timezone set on the RPi."""
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)
