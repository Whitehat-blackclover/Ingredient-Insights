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

#Improving resolution 
new_size = (img.width*2, img.height*2)
img = img.resize(new_size, Image.LANCZOS)

#Sharpening the image 
sharpness_enhancer = ImageEnhance.Sharpness(img)
img = sharpness_enhancer.enhance(0.1)

img.save('processed_test_image6.jpg')