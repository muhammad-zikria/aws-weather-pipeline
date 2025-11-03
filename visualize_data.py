import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt

# --- SETTINGS ---
DB_USERNAME = "postgres"
DB_PASSWORD = "YOUR_SAVED_PASSWORD"
DB_ENDPOINT = "YOUR_COPIED_ENDPOINT"
DB_PORT = "5432" # Default for PostgreSQL
DB_NAME = "postgres"

# --- 1. CREATE DATABASE CONNECTION ---
try:
    # Connection string
    connection_str = f"postgresql+psycopg2://{DB_USERNAME}:{DB_PASSWORD}@{DB_ENDPOINT}:{DB_PORT}/{DB_NAME}"
    engine = create_engine(connection_str)
    print("Database engine created successfully.")

    # --- 2. QUERY DATA FROM DATABASE ---
    # This is our SQL query
    sql_query = "SELECT * FROM weather_data;"
    
    # Use pandas to execute the query and load results into a DataFrame
    df = pd.read_sql(sql_query, engine)
    
    print(f"Successfully queried {len(df)} rows from the database:")
    print(df)

    # --- 3. VISUALIZE THE DATA ---
    if not df.empty:
        # Sort by timestamp just in case
        df = df.sort_values(by='timestamp')
        
        plt.figure(figsize=(10, 6))
        plt.plot(df['timestamp'], df['temperature'], marker='o') # Plot temperature
        
        plt.title(f"Temperature Over Time - {df['city'].iloc[0]}")
        plt.xlabel("Timestamp")
        plt.ylabel("Temperature (°C)")
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # This will open a new window with your chart
        print("Displaying plot...")
        plt.show()
    else:
        print("No data to plot.")

except Exception as e:
    print(f"An error occurred: {e}")