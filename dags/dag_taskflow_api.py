from datetime import datetime, timedelta
from airflow.decorators import dag, task

default_args = {
    'owner': 'Ivan Marques',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}


@dag(dag_id='DAG-API',
     default_args=default_args,
     start_date=datetime(2022, 4, 12),
     schedule_interval='@daily'
     )
def comprimentar():
    @task()
    def pergunta_nome(multiple_outputs=True):
        return {
            'nome': 'Ivan',
            'sobrenome': 'Marques'
        }

    @task()
    def pergunta_idade():
        return 34

    @task()
    def diz_ola(nome, sobrenome, idade):
        print(f'Olá {nome}-{sobrenome}, com idade de {idade} anos!')

    nome_completo = pergunta_nome()
    idade = pergunta_idade()
    diz_ola(nome=nome_completo['nome'],
                  sobrenome=nome_completo['sobrenome'],
                  idade=idade)

    dag_saudacao = comprimentar()
