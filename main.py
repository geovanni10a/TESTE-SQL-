from soap_service import *
from sql_queries import *
from time import perf_counter

# Criação da conexão com banco de dados SQL SERVER
conn = criar_conexao()
cursor = conn.cursor()

# Criação de conexão com o Webservice SOAP
clientWSDL = iniciar_conexao()

dados_paises = get_dados_paises(clientWSDL)
dados_linguagens = get_dados_monetarios(clientWSDL)
dados_continentes = get_dados_continentes(clientWSDL)
dados_linguas = get_dados_linguas(clientWSDL)

# inserção dos dados no banco de dados
try:
    start_time = perf_counter()

    inserir_dados(cursor, full_continent_data=dados_continentes, 
                full_language_data=dados_linguas, 
                full_currency_data=dados_linguagens, 
                full_countries_data=dados_paises)

    end_time = perf_counter()

    print(f'Dados inseridos com sucesso em {end_time - start_time:.2f} segundos.')

    cursor.commit()
except Exception as e:
    print('Erro ao inserir dados: ', e)
    cursor.rollback()
