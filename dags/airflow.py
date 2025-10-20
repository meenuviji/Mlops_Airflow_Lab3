from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from src.lab_wine import load_data, data_preprocessing, build_save_model, evaluate_model

# Default DAG arguments
default_args = {
    'owner': 'friend_name',  # Replace with your friend's name if needed
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=3)
}

# Define the DAG
with DAG(
    dag_id='Airflow_Lab1_WineQuality',
    default_args=default_args,
    description='Wine Quality DBSCAN Clustering + Evaluation',
    schedule_interval='@daily',
    start_date=datetime(2025, 10, 20),
    catchup=False,
    tags=['wine_quality', 'DBSCAN', 'clustering']
) as dag:

    # Task 1: Load Data
    load_data_task = PythonOperator(
        task_id='load_data',
        python_callable=load_data
    )

    # Task 2: Preprocess Data
    preprocess_task = PythonOperator(
        task_id='data_preprocessing',
        python_callable=data_preprocessing
    )

    # Task 3: Build and Save Model
    build_model_task = PythonOperator(
        task_id='build_save_model',
        python_callable=build_save_model
    )

    # Task 4: Evaluate Model
    evaluate_task = PythonOperator(
        task_id='evaluate_model',
        python_callable=evaluate_model
    )

    # Define task dependencies (DAG flow)
    load_data_task >> preprocess_task >> build_model_task >> evaluate_task