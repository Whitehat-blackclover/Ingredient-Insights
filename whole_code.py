import re
import pandas as pd
from PIL import Image, ImageEnhance
import pytesseract

# Set the path to the Tesseract OCR executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Function to improve the image quality for OCR
def image_improvement(img_path='test_image.png'):
    try:
        img = Image.open(img_path)
        img = img.convert('L')  # Convert to grayscale for OCR accuracy
        img = ImageEnhance.Contrast(img).enhance(2)  # Increase contrast
        img = img.resize((img.width * 2, img.height * 2), Image.LANCZOS)  # Resize for clarity
        img = ImageEnhance.Sharpness(img).enhance(1.5)  # Moderate sharpness increase
        processed_image_path = 'processed_test_image.png'
        img.save(processed_image_path)
        return processed_image_path
    except Exception as e:
        print(f"Error improving image: {e}")
        return None

# Function to extract text from the improved image
def image_processing(img_path='test_image.png'):
    processed_img_path = image_improvement(img_path)
    if processed_img_path:
        try:
            img = Image.open(processed_img_path)
            text = pytesseract.image_to_string(img, config='--psm 6')  # Extract text
            print("Extracted Text:", text)
            return text
        except Exception as e:
            print(f"Error in OCR processing: {e}")
    return ""

# Function to clean extracted text and parse ingredients
def text_cleaning(img_path='test_image.png'):
    extracted_text = image_processing(img_path)
    # Remove special characters, except commas and alphanumeric characters
    clean_text = re.sub(r'[^a-zA-Z0-9, ]', '', extracted_text)
    
    # Split the cleaned text into a list of ingredients
    ingredients = [i.strip().lower() for i in clean_text.split(',') if i]
    
    # Remove "ingredients" or any similar unwanted term from the start of the list
    if ingredients and 'ingredients' in ingredients[0]:
        ingredients.pop(0)
    return ingredients

# Load the cleaned database
database_path = 'cleaned_data.csv'
try:
    df_database = pd.read_csv(database_path)
except Exception as e:
    print(f"Error loading database: {e}")

# Define function to retrieve information from database based on ingredient list
def get_ingredient_info(ingredient_list):
    # Dictionary to store ingredient information
    ingredient_info = {}

    for ingredient in ingredient_list:
        # Filter database for matching ingredient
        match = df_database[df_database['ingredients_text_en'].str.contains(re.escape(ingredient), case=False, na=False)]

        if not match.empty:
            # Extract relevant info for the matched ingredient
            info = {
                'product_name': match.iloc[0]['product_name_en'] if 'product_name_en' in match.columns else None,
                'brand': match.iloc[0]['brands'] if 'brands' in match.columns else None,
                'category': match.iloc[0]['categories'] if 'categories' in match.columns else None,
                'origin': match.iloc[0]['origins'] if 'origins' in match.columns else None,
                'country': match.iloc[0]['countries'] if 'countries' in match.columns else None,
            }
            ingredient_info[ingredient] = info
        else:
            ingredient_info[ingredient] = 'No information available'

    return ingredient_info

# Run the process and fetch ingredient details
ingredient_list = text_cleaning()  # Extracted ingredients from OCR
ingredient_details = get_ingredient_info(ingredient_list)

# Print the information for each ingredient
for ingredient, details in ingredient_details.items():
    print(f"Ingredient: {ingredient.capitalize()}")
    if isinstance(details, dict):
        print("  - Product Name:", details.get('product_name', 'N/A'))
        print("  - Brand:", details.get('brand', 'N/A'))
        print("  - Category:", details.get('category', 'N/A'))
        print("  - Origin:", details.get('origin', 'N/A'))
        print("  - Country:", details.get('country', 'N/A'))
        print("  - Information:", details)
    else:
        print("  - Information:", details)
    print("\n" + "-" * 40 + "\n")