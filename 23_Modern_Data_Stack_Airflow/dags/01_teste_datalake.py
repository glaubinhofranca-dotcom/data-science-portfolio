from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from datetime import datetime

def upload_hello_world():
    # Connect to MinIO using the pre-configured connection ID
    hook = S3Hook(aws_conn_id='aws_default')
    
    # Create and upload a file directly to the Data Lake
    hook.load_string(
        string_data="Hello! If you are reading this, Airflow has successfully connected to MinIO. 🚀",
        key="teste_conexao.txt",         # Target filename
        bucket_name="landing-zone",      # Target bucket name
        replace=True
    )
    print("File uploaded successfully!")

# DAG definition
with DAG(
    '01_teste_datalake',
    start_date=datetime(2023, 1, 1),
    schedule_interval=None, # Set to None for manual triggers only
    catchup=False,
    tags=['engineering']
) as dag:

    tarefa_upload = PythonOperator(
        task_id='upload_para_minio',
        python_callable=upload_hello_world
    )