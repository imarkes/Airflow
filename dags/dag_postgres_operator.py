from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator

default_args = {
    'owner': 'Ivan Marques',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}

with DAG(
        dag_id='DAG-Bash-01',
        default_args=default_args,
        description='Task para testar o bash operator',
        start_date=datetime(2022, 4, 11),
        schedule_interval='0 0 * * *'  # min, hora, dia, mes, ano
) as dag:
    task_create = PostgresOperator(
        task_id='task_create',
        postgres_conn_id='postgres_localhost',
        sql="""
            create table if not exists dag_tests(
            dt date, 
            dag_id varchar,
            primary key(dt, dag_id)
            )
        """
    )
    task_insert = PostgresOperator(
        task_id='task_insert',
        postgres_conn_id='postgres_localhost',
        sql="""
            insert into dag_tests(dt, dag_id) values ('{{ ds }}',
            '{{dag.dag_id}}')

        """
    )

    task_create >> task_insert