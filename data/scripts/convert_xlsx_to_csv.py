import pandas as pd
from pathlib import Path

# Project root'a göre yollar
input_path = Path("data/raw/Online Retail.xlsx")
output_path = Path("data/raw/online_retail.csv")

df = pd.read_excel(input_path)

df.to_csv(output_path, index=False, encoding="utf-8")

print("CSV created successfully!")
print("Output:", output_path)
print("Shape:", df.shape)
print(df.head())