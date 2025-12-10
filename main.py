import pyodbc

def criar_conexao():
    conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost\\SQLEXPRESS;"
    "DATABASE=dblattes;"
    "Trusted_Connection=yes;"
    )

    print('Conexão criada com sucesso.')
    return pyodbc.connect(conn_str)

conn = criar_conexao()
conn.close()