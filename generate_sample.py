import pandas as pd
import numpy as np
import os

print("Generating synthetic dataset with intentional flaws for cleaning practice...")

np.random.seed(101)
n_rows = 500

# Fictional E-commerce dataset
dates = pd.date_range(start='2025-01-01', periods=n_rows)
product_categories = np.random.choice(['Electronics', 'Clothing', 'Home & Garden', 'Sports', 'Toys'], n_rows)
prices = np.random.uniform(10.0, 500.0, n_rows).round(2)
quantities = np.random.randint(1, 10, n_rows)
ratings = np.random.uniform(1.0, 5.0, n_rows).round(1)

df = pd.DataFrame({
    'Order_Date': dates,
    'Category': product_categories,
    'Price_USD': prices,
    'Quantity': quantities,
    'Customer_Rating': ratings
})

df['Total_Sales_USD'] = df['Price_USD'] * df['Quantity']

# Injecting intentional missing values (NaN) to test the Cleaning Tools
missing_idx_price = np.random.choice(n_rows, size=15, replace=False)
df.loc[missing_idx_price, 'Price_USD'] = np.nan

missing_idx_rating = np.random.choice(n_rows, size=30, replace=False)
df.loc[missing_idx_rating, 'Customer_Rating'] = np.nan

# Injecting some duplicate rows to test the Duplicate removal tool
duplicates = df.sample(10)
df = pd.concat([df, duplicates], ignore_index=True)

# Save as CSV
file_path = os.path.join(os.getcwd(), 'sample_dataset.csv')
df.to_csv(file_path, index=False)
print(f"Generated 'sample_dataset.csv' successfully at {file_path}")
