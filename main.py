import pyodbc
from soap_service import *
from sql_queries import *

def criar_conexao():
    conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost\\SQLEXPRESS;"
    "DATABASE=country_info;"
    "Trusted_Connection=yes;"
    )

    print('Conexão criada com sucesso.')
    return pyodbc.connect(conn_str)

# Teste de inserção em tabela.

conn = criar_conexao()
cursor = conn.cursor()

continent_list = get_dados_continentes()

sql_insert = criar_insert_sql('principal.continents', continent_list)

cursor.execute(sql_insert)

cursor.commit()

conn.close()