# Importing Image class from PIL module
from PIL import Image
import os


Directory = os.getcwd()
Directory = Directory.replace('\Scripts', '\Scripts\Received_Image.jpg')

print(Directory)


def CropImage():

    imageObject = Image.open(Directory)
    # print(imageObject.size)
    cropped = imageObject.crop((1850, 1850, 2150, 2150))
    cropped.save('Map_Image.jpg')
