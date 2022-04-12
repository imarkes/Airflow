from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'Ivan Marques',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}


def hello(nome, idade):
    print(f'Olá: {nome}, você tem {idade} anos!')


def name():
    return 'Ivan Marques'


def hello_xcom_pull(idade, ti):
    nome = ti.xcom_pull(task_ids='hello_name')
    print(f'Olá: {nome}, você tem {idade} anos!')


def hello_xcom_push(numero, ti):
    cidade = ti.xcom_pull(task_ids='push_endereco', key='cidade')
    endereco = ti.xcom_pull(task_ids='push_endereco', key='endereco')
    nome = ti.xcom_pull(task_ids='name')
    print(f'Olá {nome}, voce mora na cidade: {cidade} endereço: {endereco}, numero:{numero}')


def push_endereco(ti):
    ti.xcom_push(key='cidade', value='Vitoria')
    ti.xcom_push(key='endereco', value='Rua ABC')


with DAG(
        dag_id='DAG-Python-05',
        default_args=default_args,
        description='Task para testar o python operator',
        start_date=datetime(2022, 4, 11),
        schedule_interval='@daily'
) as dag:
    task1 = PythonOperator(
        task_id='hello',
        python_callable=hello,
        op_kwargs={'nome': 'Ivan Marques', 'idade': 34}
    )

    task2 = PythonOperator(
        task_id='name',
        python_callable=name
    )

    task3 = PythonOperator(
        task_id='hello_xcom_pull',
        python_callable=hello_xcom_pull,
        op_kwargs={'idade': 50}
    )

    task4 = PythonOperator(
        task_id='push_endereco',
        python_callable=push_endereco,
    )

    task5 = PythonOperator(
        task_id='hello_xcom_push',
        python_callable=hello_xcom_push,
        op_kwargs={'numero': 18}
    )

    [task1, task2] >> task3 >> [task4, task5]
