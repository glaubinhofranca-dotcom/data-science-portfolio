from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime, timedelta
import pandas as pd
import io

# Configuration
BUCKET_NAME = "landing-zone"
FILE_NAME = "daily_sales.csv"
TABLE_NAME = "sales_silver"

def load_s3_to_postgres(**kwargs):
    """
    Downloads CSV from MinIO (Bronze), transforms it (adds metadata),
    and loads it into Postgres (Silver).
    """
    # 1. Calculate the S3 Key for today (Partition)
    now = datetime.now()
    # Note: In production, use kwargs['execution_date'] for backfilling
    s3_key = f"raw/sales/year={now.year}/month={now.month:02d}/day={now.day:02d}/{FILE_NAME}"
    
    # 2. Download from MinIO
    s3_hook = S3Hook(aws_conn_id='aws_default')
    
    # Check if file exists
    if not s3_hook.check_for_key(s3_key, BUCKET_NAME):
        raise Exception(f"File not found in S3: {s3_key}")
        
    obj = s3_hook.get_key(s3_key, BUCKET_NAME)
    csv_content = obj.get()['Body'].read().decode('utf-8')
    
    # 3. Read into Pandas
    df = pd.read_csv(io.StringIO(csv_content))
    
    # 4. Transform: Add metadata (Ex: ingestion timestamp)
    df['ingested_at'] = datetime.now()
    
    # 5. Load to Postgres
    pg_hook = PostgresHook(postgres_conn_id='postgres_dw')
    
    # Idempotency: Delete data from today before inserting (to avoid duplicates)
    delete_sql = f"DELETE FROM {TABLE_NAME} WHERE date = '{now.strftime('%Y-%m-%d')}'"
    pg_hook.run(delete_sql)
    
    # Insert rows
    # Note: efficient for small/medium datasets. For big data, use COPY command.
    rows = list(df.itertuples(index=False, name=None))
    pg_hook.insert_rows(
        table=TABLE_NAME,
        rows=rows,
        target_fields=[col for col in df.columns] # Map columns automatically
    )
    print(f"Successfully loaded {len(rows)} rows into {TABLE_NAME}")

# DAG Definition
default_args = {
    'owner': 'glauber',
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

with DAG(
    '03_silver_loading',
    default_args=default_args,
    start_date=datetime(2023, 1, 1),
    schedule_interval='@daily',
    catchup=False,
    tags=['silver', 'etl']
) as dag:

    # Task 1: Create Table (DDL)
    create_table = PostgresOperator(
        task_id='create_postgres_table',
        postgres_conn_id='postgres_dw',
        sql=f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            transaction_id INT,
            date DATE,
            product VARCHAR(100),
            store VARCHAR(50),
            amount DECIMAL(10,2),
            quantity INT,
            ingested_at TIMESTAMP
        );
        """
    )

    # Task 2: ETL (Python)
    load_data = PythonOperator(
        task_id='load_s3_to_postgres',
        python_callable=load_s3_to_postgres
    )

    # Flow
    create_table >> load_data