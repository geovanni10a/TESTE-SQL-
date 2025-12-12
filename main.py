import pyodbc
from soap_service import *
from sql_queries import *

# Teste de inserção em tabela.

# Criação da conexão com banco de dados SQL SERVER
conn = criar_conexao()
cursor = conn.cursor()

# Criação de conexão com o Webservice SOAP
clientWSDL = iniciar_conexao()

# Coleta dos dados com base no código do país
country_code = 'AD'
country_full_data = get_dados_completos_paises(clientWSDL, 'AD')

country_full_monetary_data = get_dados_monetarios(clientWSDL, country_code)
country_full_continent_data = get_dados_continente(clientWSDL, country_full_data['continent_code'])
country_full_languages_data = get_dados_linguagens(clientWSDL, country_full_data['language_codes'])

# inserção dos dados coletados
inserir_dados(cursor=cursor, 
              dados_continente=country_full_continent_data, 
              dados_linguagens=country_full_languages_data, 
              dados_monetarios=country_full_monetary_data, 
              dados_totais=country_full_data)

cursor.commit()
conn.close()