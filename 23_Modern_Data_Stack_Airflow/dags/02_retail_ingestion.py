from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from datetime import datetime, timedelta
import pandas as pd
import random
import io

# Configuration
BUCKET_NAME = "landing-zone"
FILE_NAME = "daily_sales.csv"

def generate_fake_data(**kwargs):
    """
    Simulates data extraction from a sales system (SAP/Salesforce).
    Generates a DataFrame and returns the CSV as a string.
    """
    products = ['Dell Laptop', 'Iphone 15', 'LG Monitor', 'Mechanical Keyboard', 'Gaming Mouse']
    stores = ['Boston_MA', 'NewYork_NY', 'Chicago_IL', 'Austin_TX']
    
    data = []
    for _ in range(100): # Generate 100 sales records
        row = {
            'transaction_id': random.randint(10000, 99999),
            'date': datetime.now().strftime("%Y-%m-%d"),
            'product': random.choice(products),
            'store': random.choice(stores),
            'amount': round(random.uniform(100.0, 5000.0), 2),
            'quantity': random.randint(1, 5)
        }
        data.append(row)
    
    # FIXED: Create DataFrame directly from list of dicts (No JSON needed)
    df = pd.DataFrame(data)
    print(f"Generated data: {len(df)} rows.")
    
    # Save CSV to memory buffer (avoids creating files on container disk)
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    
    # Pass CSV content to the next task via XCom (Airflow memory)
    return csv_buffer.getvalue()

def upload_to_datalake(**kwargs):
    """
    Takes the generated CSV and saves it to MinIO (S3) with date partitioning.
    Ex: landing-zone/raw/sales/year=2026/month=01/day=29/daily_sales.csv
    """
    # Retrieve CSV from previous task
    ti = kwargs['ti']
    csv_content = ti.xcom_pull(task_ids='generate_sales_data')
    
    # Define path (Partition Key)
    now = datetime.now()
    s3_key = f"raw/sales/year={now.year}/month={now.month:02d}/day={now.day:02d}/{FILE_NAME}"
    
    # Connect and Upload
    hook = S3Hook(aws_conn_id='aws_default')
    hook.load_string(
        string_data=csv_content,
        key=s3_key,
        bucket_name=BUCKET_NAME,
        replace=True
    )
    print(f"File saved at: s3://{BUCKET_NAME}/{s3_key}")

# DAG Definition
default_args = {
    'owner': 'glauber',
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

with DAG(
    '02_retail_ingestion',
    default_args=default_args,
    start_date=datetime(2023, 1, 1),
    schedule_interval='@daily', 
    catchup=False,
    tags=['bronze', 'ingestion']
) as dag:

    task_generate = PythonOperator(
        task_id='generate_sales_data',
        python_callable=generate_fake_data
    )

    task_upload = PythonOperator(
        task_id='upload_to_datalake',
        python_callable=upload_to_datalake,
        provide_context=True
    )

    # Flow: Generate -> Upload
    task_generate >> task_upload