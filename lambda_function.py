import os
import requests
import json
import pandas as pd
from datetime import datetime
import boto3
from sqlalchemy import create_engine

def lambda_handler(event, context):
    
    # --- 1. GET ALL ENVIRONMENT VARIABLES ---
    # These will be set in the Lambda configuration
    try:
        API_KEY = os.environ['API_KEY']
        CITY = os.environ['CITY']
        AWS_S3_BUCKET = os.environ['AWS_S3_BUCKET']
        DB_USERNAME = os.environ['DB_USERNAME']
        DB_PASSWORD = os.environ['DB_PASSWORD']
        DB_ENDPOINT = os.environ['DB_ENDPOINT']
        DB_NAME = os.environ['DB_NAME']
    except KeyError as e:
        print(f"Error: Environment variable {e} not set.")
        return { 'statusCode': 500, 'body': json.dumps(f"Error: Environment variable {e} not set.") }

    # Define other constants
    URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
    LOCAL_FILE_PATH = '/tmp/weather_data.csv' # Lambda uses /tmp for temporary storage
    S3_KEY = f'raw/weather_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    
    # --- 2. FETCH DATA FROM API & TRANSFORM ---
    try:
        response = requests.get(URL)
        response.raise_for_status()
        data = response.json()

        weather = {
            "city": CITY,
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "pressure": data["main"]["pressure"],
            "weather": data["weather"][0]["description"],
            "timestamp": datetime.now()
        }
        df = pd.DataFrame([weather])
        print("Data fetched and transformed.")
        
        # Save to Lambda's temporary storage
        df.to_csv(LOCAL_FILE_PATH, index=False)
        print(f"Data saved to {LOCAL_FILE_PATH}")
        
    except Exception as e:
        print(f"Error during API fetch or transform: {e}")
        return { 'statusCode': 500, 'body': json.dumps(f"Error during API fetch: {e}") }

    # --- 3. UPLOAD TO S3 ---
    try:
        s3 = boto3.client('s3') # No keys needed, Lambda will use its IAM Role
        s3.upload_file(LOCAL_FILE_PATH, AWS_S3_BUCKET, S3_KEY)
        print(f"File uploaded to S3: {S3_KEY}")
    except Exception as e:
        print(f"Error uploading to S3: {e}")
        return { 'statusCode': 500, 'body': json.dumps(f"Error uploading to S3: {e}") }
        
    # --- 4. LOAD INTO RDS (POSTGRESQL) ---
    try:
        connection_str = f"postgresql+psycopg2://{DB_USERNAME}:{DB_PASSWORD}@{DB_ENDPOINT}:5432/{DB_NAME}"
        engine = create_engine(connection_str)
        
        df['timestamp'] = pd.to_datetime(df['timestamp']) # Ensure correct type for SQL
        
        df.to_sql('weather_data', engine, if_exists='append', index=False)
        print("Data inserted into RDS successfully.")
        
    except Exception as e:
        print(f"Error loading to RDS: {e}")
        return { 'statusCode': 500, 'body': json.dumps(f"Error loading to RDS: {e}") }

    # --- 5. SUCCESS RESPONSE ---
    return {
        'statusCode': 200,
        'body': json.dumps('Weather data ETL completed successfully!')
    }