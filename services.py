from soap_service import *
from sql_queries import *
from time import perf_counter

def realizar_insercao(cursor: pyodbc.Cursor, clientWSDL: Client, requested_countries: list = []) -> None:
    if not requested_countries:
        inserir_todos_dados(cursor, clientWSDL)
    else:
        inserir_dados_informados(cursor, clientWSDL, codigo_pais_list=requested_countries)

def inserir_todos_dados(cursor: pyodbc.Cursor, clientWSDL: Client) -> None:
    dados_paises = get_dados_paises(clientWSDL)
    dados_linguagens = get_dados_monetarios(clientWSDL)
    dados_continentes = get_dados_continentes(clientWSDL)
    dados_linguas = get_dados_linguas(clientWSDL)

    # inserção dos dados no banco de dados
    try:
        start_time = perf_counter()

        inserir_dados_db(cursor, full_continent_data=dados_continentes, 
                    full_language_data=dados_linguas, 
                    full_currency_data=dados_linguagens, 
                    full_countries_data=dados_paises)

        end_time = perf_counter()

        print(f'Dados inseridos com sucesso em {end_time - start_time:.2f} segundos.')

        cursor.commit()
    except Exception as e:
        print('Erro ao inserir dados: ', e)
        cursor.rollback()  

def inserir_dados_informados(cursor: pyodbc.Cursor, clientWSDL: Client, /, codigo_pais_list: list) -> None:
    dados_todos_paises = get_dados_paises(clientWSDL)
    dados_todos_continentes = get_dados_continentes(clientWSDL)
    dados_todas_linguagens = get_dados_linguas(clientWSDL)
    dados_todas_moedas = get_dados_monetarios(clientWSDL)

    # filtragem de dados por países requisitados
    dados_paises_requisitados = [country for country in dados_todos_paises if country['iso_code'] in codigo_pais_list]

    codigos_linguagens_requisitadas = []
    codigos_continentes_requisitados = []
    codigos_monetarios_requisitados = []

    for pais in dados_paises_requisitados:
        for lang in pais['languages']:
            codigos_linguagens_requisitadas.append(lang['sISOCode'])

        codigos_continentes_requisitados.append(pais['continent_code'])
        codigos_monetarios_requisitados.append(pais['currency_code'])


    dados_linguagens_requisitadas = [lang for lang in dados_todas_linguagens if lang['sISOCode'] in codigos_linguagens_requisitadas]
    dados_continentes_requisitados = [cont for cont in dados_todos_continentes if cont['sCode'] in codigos_continentes_requisitados]
    dados_monetarios_requisitados = [curr for curr in dados_todas_moedas if curr['sISOCode'] in codigos_monetarios_requisitados]

    print(dados_paises_requisitados)
    print('---')
    print(dados_continentes_requisitados)
    print('---')
    print(dados_monetarios_requisitados)
    print('---')
    print(dados_linguagens_requisitadas)

    # inserção dos dados filtrados
    try:
        start_time = perf_counter() 
        inserir_dados_db(cursor, 
                        full_continent_data=dados_continentes_requisitados,
                        full_countries_data=dados_paises_requisitados,
                        full_currency_data=dados_monetarios_requisitados,
                        full_language_data=dados_linguagens_requisitadas)
        end_time = perf_counter()

        print(f'Dados inseridos com sucesso em {end_time - start_time:.2f} segundos.')
        cursor.commit()
    except Exception as e:
        print('Erro ao inserir dados: ', e)
        cursor.rollback()

    

    