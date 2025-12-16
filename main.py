import pyodbc
from soap_service import *
from sql_queries import *
from time import perf_counter

# Teste de inserção em tabela.

# Criação da conexão com banco de dados SQL SERVER
conn = criar_conexao()
cursor = conn.cursor()

# Criação de conexão com o Webservice SOAP
clientWSDL = iniciar_conexao()

# Coleta dos dados com base no código do país
try:
    start_time = perf_counter()
    print('-'*30)
    for country_code in get_codigos_paises(clientWSDL):
        country_full_data = get_dados_completos_paises(clientWSDL, country_code)

        country_full_monetary_data = get_dados_monetarios(clientWSDL, country_code)
        country_full_continent_data = get_dados_continente(clientWSDL, country_full_data['continent_code'])
        country_full_languages_data = country_full_data['languages']

        # inserção dos dados coletados
        inserir_dados(cursor, 
                    dados_continente=country_full_continent_data, 
                    dados_linguagens=country_full_languages_data, 
                    dados_monetarios=country_full_monetary_data, 
                    dados_totais_pais=country_full_data)  
    print('-'*30)
    end_time = perf_counter()

    print(f'Tempo total de execução: {(end_time - start_time):.2f} segundos.')

    cursor.commit()
except Exception as e:
    conn.rollback()
    print('Erro ao inserir dados: ', e)

cursor.close()
conn.close()