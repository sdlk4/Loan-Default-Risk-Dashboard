import os
import pandas as pd
import mysql.connector
from dotenv import load_dotenv

# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# -----------------------------
# Connect to MySQL
# -----------------------------
connection = mysql.connector.connect(
    host=DB_HOST,
    port=DB_PORT,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME
)

cursor = connection.cursor()
print("Connected to MySQL.")

# -----------------------------
# Load RAW table into pandas
# -----------------------------
query = "SELECT * FROM application_train_raw"
df = pd.read_sql(query, connection)
print("Loaded raw data:", df.shape)

# -----------------------------
# BASIC CLEANING STEPS
# -----------------------------

# 1. Replace weird negative days (DAYS_EMPLOYED = 365243 often means 'not employed')
df["DAYS_EMPLOYED"] = df["DAYS_EMPLOYED"].replace({365243: None})

# 2. Convert income and credit to numeric safely
for col in ["AMT_INCOME_TOTAL", "AMT_CREDIT", "AMT_ANNUITY", "AMT_GOODS_PRICE"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# 3. Fill categorical NULLs with "Unknown"
cat_cols = df.select_dtypes(include="object").columns
df[cat_cols] = df[cat_cols].fillna("Unknown")

# 4. Fill numeric NULLs with median
num_cols = df.select_dtypes(include=["int64", "float64"]).columns
df[num_cols] = df[num_cols].fillna(df[num_cols].median())

print("Data cleaned:", df.shape)

# -----------------------------
# CREATE CLEAN TABLE IN MYSQL
# -----------------------------

cursor.execute("DROP TABLE IF EXISTS application_train_cleaned;")

columns_with_types = ", ".join([f"`{col}` TEXT" for col in df.columns])
create_clean_table = f"""
CREATE TABLE application_train_cleaned (
    {columns_with_types}
);
"""

cursor.execute(create_clean_table)
connection.commit()
print("Clean table created.")

# -----------------------------
# FAST BULK INSERT CLEANED DATA
# -----------------------------
from mysql.connector import Error

chunk_size = 10000
columns = ", ".join([f"`{col}`" for col in df.columns])
placeholders = ", ".join(["%s"] * len(df.columns))
insert_query = f"INSERT INTO application_train_cleaned ({columns}) VALUES ({placeholders})"

print("Starting fast insert...")

try:
    for start in range(0, len(df), chunk_size):
        end = start + chunk_size
        chunk = df.iloc[start:end].astype(object)
        data = [tuple(row) for row in chunk.values]

        cursor.executemany(insert_query, data)
        connection.commit()

        print(f"Inserted rows {start} to {end}")

    print("Cleaned data inserted!")

except Error as e:
    print("Error during insert:", e)

cursor.close()
connection.close()

print("Done!")
