from PIL import Image
import math

def cropImage(image):
    """Crops all transparent space around an image. Returns that cropped image."""

    # Get the bounding box of the image. Aka, boundries of what's non-transparent.
    bbox = image.getbbox()

    # Crop the image to the contents of the bounding box.
    image = image.crop(bbox)

    # Determine the width and height of the cropped image.
    (width, height) = image.size
    
    # Create a new image object for the output image.
    croppedImage = Image.new("RGB", (width, height), (0,0,0,255))

    # Paste the cropped image onto the new image.
    croppedImage.paste(image)

    return croppedImage

def resizeImage(image):
    aspectRatio = image.height / image.width 
    width = 30
    height = math.floor(width * aspectRatio)
    return image.resize((width, height))
