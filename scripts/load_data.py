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
try:
    connection = mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    print("MySQL connection successful!")
except Exception as e:
    print("Connection failed:", e)
    exit()

cursor = connection.cursor()

# -----------------------------
# Create raw table
# -----------------------------
create_table_query = """
CREATE TABLE IF NOT EXISTS application_train_raw (
    SK_ID_CURR INT,
    TARGET INT,
    NAME_CONTRACT_TYPE VARCHAR(50),
    CODE_GENDER VARCHAR(10),
    FLAG_OWN_CAR VARCHAR(5),
    FLAG_OWN_REALTY VARCHAR(5),
    CNT_CHILDREN INT,
    AMT_INCOME_TOTAL DOUBLE,
    AMT_CREDIT DOUBLE,
    AMT_ANNUITY DOUBLE,
    AMT_GOODS_PRICE DOUBLE,
    NAME_TYPE_SUITE VARCHAR(50),
    NAME_INCOME_TYPE VARCHAR(50),
    NAME_EDUCATION_TYPE VARCHAR(50),
    NAME_FAMILY_STATUS VARCHAR(50),
    NAME_HOUSING_TYPE VARCHAR(50),
    DAYS_BIRTH INT,
    DAYS_EMPLOYED INT,
    DAYS_REGISTRATION DOUBLE,
    DAYS_ID_PUBLISH INT,
    OWN_CAR_AGE DOUBLE,
    FLAG_MOBIL INT,
    FLAG_EMP_PHONE INT,
    FLAG_WORK_PHONE INT,
    FLAG_CONT_MOBILE INT,
    FLAG_PHONE INT,
    FLAG_EMAIL INT,
    REGION_RATING_CLIENT INT,
    REGION_RATING_CLIENT_W_CITY INT,
    -- We are NOT listing all 120+ columns now.
    -- We'll load all columns dynamically using pandas.
    dummy_col INT
);
"""

# Create an empty placeholder table first
try:
    cursor.execute(create_table_query)
    print("Raw table created (placeholder).")
except Exception as e:
    print("Failed to create table:", e)

connection.commit()

# -----------------------------
# Load CSV using pandas
# -----------------------------
csv_path = "C:\\Users\\srika\\OneDrive\\Desktop\\Loan_default_risk\\data\\application_train.csv"

df = pd.read_csv(csv_path)

print(f"CSV loaded: {df.shape[0]} rows, {df.shape[1]} columns")

# -----------------------------
# Load full dataframe into MySQL
# -----------------------------
# Drop placeholder table and recreate dynamically
cursor.execute("DROP TABLE IF EXISTS application_train_raw;")

# Create table automatically
columns_with_types = ", ".join([f"`{col}` TEXT" for col in df.columns])
create_dynamic_table = f"CREATE TABLE application_train_raw ({columns_with_types});"

cursor.execute(create_dynamic_table)
connection.commit()
print("Dynamic raw table created with all columns.")

# Insert data row-by-row
for _, row in df.iterrows():
    vals = tuple(row.astype(str).fillna("NULL"))
    placeholders = ", ".join(["%s"] * len(vals))
    insert_query = f"INSERT INTO application_train_raw VALUES ({placeholders})"
    cursor.execute(insert_query, vals)

connection.commit()
print("All data inserted into MySQL!")

cursor.close()
connection.close()

print("Done!")
