import pytesseract
import cv2
import matplotlib.pyplot as plt
from PIL import Image
from pytesseract import image_to_string


def convert_image_to_string(png):
    image = Image.open(png)
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    string = pytesseract.image_to_string(image)
    print(string)
    
convert_image_to_string('media/test.png')
