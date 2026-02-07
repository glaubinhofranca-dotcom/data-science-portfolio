from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datetime import datetime, timedelta

# SQL to create the aggregated table (Business Logic)
CREATE_GOLD_SQL = """
DROP TABLE IF EXISTS sales_by_store;

CREATE TABLE sales_by_store AS
SELECT
    store,
    date,
    COUNT(transaction_id) as total_transactions,
    SUM(amount) as total_revenue,
    SUM(quantity) as total_items_sold,
    NOW() as calculated_at
FROM sales_silver
GROUP BY store, date;
"""

default_args = {
    'owner': 'glauber',
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

with DAG(
    '04_gold_analytics',
    default_args=default_args,
    start_date=datetime(2023, 1, 1),
    schedule_interval='@daily',
    catchup=False,
    tags=['gold', 'analytics']
) as dag:

    # Airflow sends this SQL directly to the Postgres instance in Docker
    calculate_kpis = PostgresOperator(
        task_id='calculate_sales_by_store',
        postgres_conn_id='postgres_dw',
        sql=CREATE_GOLD_SQL
    )

    calculate_kpis