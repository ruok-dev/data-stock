from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import requests

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def generate_report():
    # In a real scenario, this would call the API or DB directly
    # and save the report to a storage (S3, local disk, etc.)
    print("Generating daily stock report...")
    # Example: response = requests.get("http://backend:8000/api/v1/analytics/reports/turnover")
    # with open("/app/reports/report.csv", "w") as f: f.write(response.text)

with DAG(
    'daily_stock_report',
    default_args=default_args,
    description='A simple DAG to generate daily stock reports',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['stock'],
) as dag:

    report_task = PythonOperator(
        task_id='generate_report',
        python_callable=generate_report,
    )

    report_task
