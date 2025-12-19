# AWS-Based Data Engineering Pipeline: Weather Analytics

## Project Overview

This project is a complete, end-to-end data pipeline built entirely on Amazon Web Services (AWS). It automatically fetches real-time weather data from the OpenWeatherMap API, processes it, and stores it in a cloud-based data lake (S3) and a relational database (RDS) for analytics. The entire process is automated and runs daily using a serverless AWS Lambda function.

This project demonstrates core data engineering skills:
* **Data Ingestion:** Collecting data from a third-party API.
* **Data Processing:** Cleaning, transforming, and structuring data with Python and Pandas.
* **Cloud Storage:** Implementing a data lake (S3) for raw data and a data warehouse (RDS) for structured data.
* **Automation:** Orchestrating the pipeline in a serverless, event-driven architecture (Lambda + EventBridge).

---

## Technical Architecture

The pipeline follows a standard Extract, Transform, Load (ETL) process:

1.  **Extract:** An **AWS EventBridge** (CloudWatch Events) trigger runs on a daily schedule (`rate(1 day)`).
2.  **Transform:** The trigger invokes an **AWS Lambda** function. This serverless function runs a Python script that:
    * Fetches real-time weather data from the **OpenWeatherMap API**.
    * Cleans and structures the data using the **Pandas** library.
3.  **Load:** The Python script then performs two loading operations:
    * **Load to S3:** The raw (or lightly processed) data is saved as a `.csv` file to an **AWS S3 bucket**, which acts as our data lake.
    * **Load to RDS:** The structured data is loaded into a `weather_data` table in an **AWS RDS** (PostgreSQL) database, making it available for SQL queries and analytics.

## Tools & Technologies

* **Cloud Provider:** AWS (Amazon Web Services)
* **Data Ingestion:** `requests` (Python)
* **Data Processing:** `pandas` (Python)
* **Data Lake:** AWS S3
* **Database:** AWS RDS (PostgreSQL)
* **Serverless Computing:** AWS Lambda
* **Orchestration/Scheduling:** AWS EventBridge (CloudWatch Events)
* **Infrastructure as Code (partial):** `boto3` (Python SDK for AWS)
* **Database Connection:** `sqlalchemy`, `psycopg2-binary`

---

## Project Results

The pipeline successfully runs, and the data can be queried from the PostgreSQL database to perform analytics.

<img width="1626" height="524" alt="image" src="https://github.com/user-attachments/assets/17461349-e179-4145-bf6d-2bbd4416ea54" />



### 1. Successful Pipeline Execution

The AWS Lambda function runs successfully on its daily schedule, with logs showing each step of the ETL process.

<img width="1075" height="396" alt="image" src="https://github.com/user-attachments/assets/42aa675e-a427-479a-be0b-e998ea90ad99" />



### 2. Data Visualization

A simple Python script (`visualize_data.py`) can connect to the live RDS database, query the data using SQL, and plot the results with `matplotlib`.

<img width="1003" height="669" alt="Screenshot 2025-11-03 021307" src="https://github.com/user-attachments/assets/816e4b53-26f2-4786-ba79-6ca9c679ea09" />


---

## How to Run (Summary of Setup)

This project is not intended to be cloned and run directly, as it requires a secure AWS setup. The key configuration steps were:

1.  **AWS Setup:**
    * Create an S3 bucket for data storage.
    * Launch an RDS PostgreSQL instance (Free Tier).
    * Configure the RDS Security Group (firewall) to allow public access.
2.  **Local Scripts (Initial Test):**
    * `get_weather.py`: Fetches API data and saves it locally.
    * `upload_to_s3.py`: Uploads the local file to S3.
    * `load_to_rds.py`: Loads the local file into the RDS database.
3.  **Automation (AWS Lambda):**
    * Consolidate all Python scripts into a single `lambda_function.py`.
    * Create a `.zip` deployment package containing the script and all dependencies (Pandas, Boto3, etc.), ensuring Linux-compatible binaries.
    * Create an IAM Role for the Lambda with `AmazonS3FullAccess` and `AmazonRDSFullAccess` permissions.
    * Create the Lambda function, upload the `.zip` file from S3, and set all API keys and database passwords as secure Environment Variables.
    * Create an EventBridge trigger to run the function on a daily schedule.
