import boto3
import os

# --- SETTINGS ---
AWS_ACCESS_KEY = "YOUR_AWS_ACCESS_KEY"
AWS_SECRET_KEY = "YOUR_AWS_SECRET_KEY"
AWS_S3_BUCKET = "weather-data-zikria"

# The local file we want to upload
LOCAL_FILE_PATH = 'weather_data.csv'

# The path we want to save the file to in S3
# 'raw/' is like a folder, and we'll use the same filename
S3_KEY = 'raw/weather_data.csv' 

# --- 1. CONNECT TO S3 ---
try:
    s3 = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY
    )
    print("Connected to S3 successfully!")

    # --- 2. UPLOAD FILE ---
    s3.upload_file(LOCAL_FILE_PATH, AWS_S3_BUCKET, S3_KEY)
    
    print(f"File '{LOCAL_FILE_PATH}' uploaded to S3 bucket '{AWS_S3_BUCKET}' as '{S3_KEY}' successfully!")

except FileNotFoundError:
    print(f"Error: The file '{LOCAL_FILE_PATH}' was not found.")
except Exception as e:
    print(f"An error occurred: {e}")