import pandas as pd
from sqlalchemy import create_engine, text
from pathlib import Path
from getpass import getpass

csv_path = Path("data/raw/online_retail.csv")

DB_USER = "postgres"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "customer_lens"

password = getpass("PostgreSQL password: ")

engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

print("Reading CSV...")
df = pd.read_csv(csv_path, dtype=str)

# Kolon isimlerini bizim SQL standardımıza çeviriyoruz
df = df.rename(
    columns={
        "InvoiceNo": "invoice_no",
        "StockCode": "stock_code",
        "Description": "description",
        "Quantity": "quantity",
        "InvoiceDate": "invoice_date",
        "UnitPrice": "unit_price",
        "CustomerID": "customer_id",
        "Country": "country",
    }
)

expected_columns = [
    "invoice_no",
    "stock_code",
    "description",
    "quantity",
    "invoice_date",
    "unit_price",
    "customer_id",
    "country",
]

df = df[expected_columns]

print("Rows:", len(df))
print(df.head())

with engine.begin() as conn:
    conn.execute(text("DROP TABLE IF EXISTS online_retail_raw;"))
    conn.execute(
        text(
            """
            CREATE TABLE online_retail_raw (
                invoice_no TEXT,
                stock_code TEXT,
                description TEXT,
                quantity TEXT,
                invoice_date TEXT,
                unit_price TEXT,
                customer_id TEXT,
                country TEXT
            );
            """
        )
    )

print("Loading to PostgreSQL...")
df.to_sql(
    "online_retail_raw",
    engine,
    schema="public",
    if_exists="append",
    index=False,
    chunksize=10000,
    method="multi",
)

print("Done! Data loaded into public.online_retail_raw")