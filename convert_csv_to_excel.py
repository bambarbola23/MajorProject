import pandas as pd
import os

csv_path = r"d:\Projects 2026 All\Major Project\dataset\master_raw_dataset.csv"
excel_path = r"d:\Projects 2026 All\Major Project\dataset\master_raw_dataset.xlsx"

print("Loading CSV file...")
df = pd.read_csv(csv_path)

print(f"Loaded {len(df)} rows. Converting to Excel...")
df.to_excel(excel_path, index=False, engine='openpyxl')

print("Successfully generated master_raw_dataset.xlsx!")

# Also convert one.csv if present
one_csv = r"d:\Projects 2026 All\Major Project\dataset\one.csv"
one_xlsx = r"d:\Projects 2026 All\Major Project\dataset\one.xlsx"
if os.path.exists(one_csv):
    df_one = pd.read_csv(one_csv)
    df_one.to_excel(one_xlsx, index=False, engine='openpyxl')
    print("Successfully generated one.xlsx!")
