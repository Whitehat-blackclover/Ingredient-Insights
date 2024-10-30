import re
from PIL import Image
from PIL import ImageEnhance
from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def image_improvement():
    img_path = 'test_image.png'
    img = Image.open(img_path)
    img = img.convert('L')
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2)
    new_size = (img.width*2, img.height*2)
    img = img.resize(new_size, Image.LANCZOS)
    sharpness_enhancer = ImageEnhance.Sharpness(img)
    img = sharpness_enhancer.enhance(0.1)

    processed_image_path = 'processed_test_image.png'
    img.save(processed_image_path)
    return processed_image_path 

def image_processing():
    img_path = image_improvement()
    img = Image.open(img_path)
    text = pytesseract.image_to_string(img)
    print("Extracted Text: ",text)
    return text 

def text_cleaning():
    extracted_text = image_processing()
    clean_text = re.sub(r'[^a-zA-Z0-9, ]', '', extracted_text)
    ingredients = [i.strip() for i in clean_text.split(',')]
    print(ingredients)

text_cleaning()