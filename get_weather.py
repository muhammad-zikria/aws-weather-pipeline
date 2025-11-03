import requests
import json
import pandas as pd
from datetime import datetime

# --- SETTINGS ---
API_KEY = "YOUR_OPENWEATHERMAP_API_KEY"  
CITY = "Berlin"
URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

# --- 1. FETCH DATA FROM API ---
try:
    response = requests.get(URL)
    response.raise_for_status()  # Raises an error for bad responses (4xx or 5xx)
    data = response.json()

    # --- 2. CLEAN AND TRANSFORM DATA ---
    # We extract only the data we care about
    weather = {
        "city": CITY,
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "pressure": data["main"]["pressure"],
        "weather": data["weather"][0]["description"],
        "timestamp": datetime.now()  # Get the current time
    }

    # --- 3. CONVERT TO PANDAS DATAFRAME ---
    df = pd.DataFrame([weather])
    print("Data fetched and transformed:")
    print(df)

    # --- 4. SAVE LOCALLY ---
    df.to_csv("weather_data.csv", index=False)
    print("Data saved to weather_data.csv successfully!")

except requests.exceptions.HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")
except requests.exceptions.RequestException as req_err:
    print(f"A request error occurred: {req_err}")
except KeyError as key_err:
    print(f"Error: Could not find key {key_err} in API response. Response was: {data}")
except Exception as err:
    print(f"An other error occurred: {err}")