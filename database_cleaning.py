import pandas as pd

# Load the CSV with a tab delimiter
file_path = 'data.csv'
df = pd.read_csv(file_path, delimiter='\t')

# Select relevant columns only (e.g., product name, ingredients, and other fields of interest)
columns_of_interest = [
    'product_name_en', 'ingredients_text_en', 'brands', 
    'categories', 'labels', 'origins', 'countries'
]
df_filtered = df[columns_of_interest]

# Drop rows where all selected columns are NaN
df_filtered.dropna(how='all', inplace=True)

# Save the cleaned data if needed
df_filtered.to_csv('cleaned_data.csv', index=False)

print(df_filtered.head())
