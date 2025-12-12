import pyodbc

def criar_conexao():
    conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost\\SQLEXPRESS;"
    "DATABASE=countries_info;"
    "Trusted_Connection=yes;"
    )

    print('Conexão criada com sucesso.')

    return pyodbc.connect(conn_str)

# função incompleta
def inserir_dados(cursor, dados_continente, dados_linguagens, dados_monetarios, dados_totais):
    inserir_dados_continente(cursor, dados_continente)

# insere dados da tabela de continentes, e deve retornar o id (incompleta)
def inserir_dados_continente(cursor: pyodbc.Cursor, continent_data: dict) -> int:
    sql_insert = "INSERT INTO country_info.continents (sName, sCode) VALUES (?, ?);"
    cursor.execute(sql_insert, (continent_data['sName'], continent_data['sCode']))
