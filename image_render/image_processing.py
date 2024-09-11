from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

#Image Path
img_path = 'processed_test_image6.jpg'

#Opening the image using pillow
img = Image.open(img_path)

#Use of Tesseract to extract text
text = pytesseract.image_to_string(img)

print("Extracted Text: ",text)