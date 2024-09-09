from PIL import Image
from PIL import ImageEnhance

#load image
img_path = 'test_image.jpg'
img = Image.open(img_path)

#converting to grayscale
img = img.convert('L')

#Contrast Enhancing
enhancer = ImageEnhance.Contrast(img)
img = enhancer.enhance(2)

img.save('processed_test_image.jpg')