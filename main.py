from soap_service import iniciar_conexao
from services import *
from sql_queries import criar_conexao
from time import perf_counter

# Criação da conexão com banco de dados SQL SERVER
conn = criar_conexao()
cursor = conn.cursor()

# Criação de conexão com o Webservice SOAP
clientWSDL = iniciar_conexao()

# Inserção de todos os dados do WS no banco de dados
realizar_insercao(cursor, clientWSDL)

# Inserção de dados específicos de países informados
#realizar_insercao(cursor, clientWSDL, requested_countries=['AD', 'BR', 'PT'])

cursor.close()
conn.close()
