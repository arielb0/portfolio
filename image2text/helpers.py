from PIL import Image
from pytesseract import pytesseract

def get_text_from_image(image_file, lang)->str:
    '''
        Given a image file return the embebed text.
    '''

    return pytesseract.image_to_string(Image.open(image_file), lang=lang)