from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from datetime import datetime, timedelta
from docker.types import Mount

default_args = {
    'owner': 'Quang',
    'retries': 3,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    dag_id= 'run_elt_dbt',
    default_args=default_args,
    start_date=datetime(2025,7 , 1),
    schedule_interval='@daily'
) as dag:
    run_etl = DockerOperator(
        task_id='run_etl',
        image='project_de-etl',
        command='python load_data/load_data_scapper.py',
        working_dir='/app',
        docker_url='unix://var/run/docker.sock',
        network_mode='project_de_default',
        do_xcom_push=False
    )
    
    run_dbt = DockerOperator(
        task_id='run_dbt',
        image='project_de-dbt',
        command='run --profiles-dir . --project-dir .',
        working_dir='/app',
        docker_url='unix://var/run/docker.sock',
        network_mode='project_de_default',
        do_xcom_push=False
    )
    
    run_etl >> run_dbt
