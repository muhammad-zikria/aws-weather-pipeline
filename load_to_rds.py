import pandas as pd
from sqlalchemy import create_engine
import os

# --- SETTINGS ---
DB_USERNAME = "postgres"
DB_PASSWORD = "YOUR_SAVED_PASSWORD"
DB_ENDPOINT = "YOUR_COPIED_ENDPOINT"
DB_PORT = "5432" 
DB_NAME = "postgres"

LOCAL_FILE_PATH = 'weather_data.csv'

# --- 1. READ LOCAL CSV FILE ---
try:
    df = pd.read_csv(LOCAL_FILE_PATH)
    
    # We must convert the timestamp string back to a datetime object
    # so that SQL knows how to store it correctly.
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    print(f"Read {len(df)} rows from {LOCAL_FILE_PATH}")

    # --- 2. CREATE DATABASE CONNECTION ---
    # Connection string format: "postgresql+psycopg2://user:password@host:port/dbname"
    connection_str = f"postgresql+psycopg2://{DB_USERNAME}:{DB_PASSWORD}@{DB_ENDPOINT}:{DB_PORT}/{DB_NAME}"
    
    engine = create_engine(connection_str)
    print("Database engine created successfully.")

    # --- 3. LOAD DATAFRAME INTO SQL DATABASE ---
    # 'weather_data' will be the name of the table in our SQL database.
    # if_exists='append' means we will add new rows every time we run this.
    df.to_sql('weather_data', engine, if_exists='append', index=False)
    
    print("Data inserted into RDS successfully!")

except FileNotFoundError:
    print(f"Error: The file '{LOCAL_FILE_PATH}' was not found.")
except Exception as e:
    print(f"An error occurred: {e}")