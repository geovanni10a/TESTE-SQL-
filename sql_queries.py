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

def inserir_dados(cursor, /, dados_continente, dados_linguagens, dados_monetarios, dados_totais_pais):
    fk_continente = inserir_dados_continente(cursor, dados_continente)
    fk_monetario = inserir_dados_monetarios(cursor, dados_monetarios)
    language_ids = inserir_dados_linguagens(cursor, dados_linguagens)

    inserir_dados_pais(cursor, dados_totais_pais, fk_monetario, fk_continente)
    ajustar_lang_countries(cursor, dados_totais_pais['iso_code'], language_ids)

def inserir_dados_pais(cursor: pyodbc.Cursor, country_data: dict, fk_currency: int, fk_continent: int):
    values_to_insert = {'sCode': country_data['iso_code'],
              'sName': country_data['name'],
              'capitalCity': country_data['capital_city'],
              'phoneCode': country_data['phone_code'],
              'flagPath': country_data['flag'],
              'fkCurrency': fk_currency,
              'fkContinent': fk_continent
              }
    

    sql_insert = f"INSERT INTO country_info.countries ({', '.join(values_to_insert.keys())}) VALUES (?, ?, ?, ?, ?, ?, ?);"

    print('País adicionado: ', country_data['name'])

    try:
        cursor.execute(sql_insert, tuple(values_to_insert.values()))
    except pyodbc.IntegrityError as e:
        print('País não adicionado: ', country_data['name'])
        raise 

# insere dados da tabela de continentes, e deve retornar o id do continente (incompleta)
def inserir_dados_continente(cursor: pyodbc.Cursor, continent_data: dict) -> int:
    sql_insert = "INSERT INTO country_info.continents (sCode, sName) VALUES (?, ?);"
    try:
        cursor.execute(sql_insert, (continent_data['sCode'], continent_data['sName']))

        cursor.execute("SELECT id FROM country_info.continents WHERE sCode = ?", (continent_data['sCode']))
        row = cursor.fetchone()
        if row:
            print('Continente adicionado: ', continent_data['sName'])
            return row.id
    except pyodbc.IntegrityError as e:
        cursor.execute("SELECT id FROM country_info.continents WHERE sCode = ?", (continent_data['sCode']))
        row = cursor.fetchone()
        if row:
            print('Continente já existente na base de dados: ', continent_data['sName'])
            return row.id
    
# insere dados da tabela de currencies, e deve retornar o id do continente (incompleta)
def inserir_dados_monetarios(cursor: pyodbc.Cursor, currency_data: dict) -> int:
    sql_insert = "INSERT INTO country_info.currencies (sCode, sName) VALUES (?, ?);"
    try:
        cursor.execute(sql_insert, (currency_data['sISOCode'], currency_data['sName']))

        cursor.execute("SELECT id FROM country_info.currencies WHERE sCode = ?", (currency_data['sISOCode']))
        row = cursor.fetchone()
        if row:
            print('Unidade Monetária adicionada: ', currency_data['sName'])
            return row.id
    except pyodbc.IntegrityError as e:
        print('Currency não adicionada: ')
        cursor.execute("SELECT id FROM country_info.currencies WHERE sCode = ?", (currency_data['sISOCode']))
        row = cursor.fetchone()
        if row:
            print('Unidade Monetária já existente no banco de dados: ', currency_data['sName'])
            return row.id
    
def inserir_dados_linguagens(cursor: pyodbc.Cursor, language_data: dict):
    if len(language_data) == 0:
        return [] 

    sql_insert = "INSERT INTO country_info.languages (sCode, sName) VALUES (?, ?);"

    languages_ids = []
        
    for lang in language_data:
        try: 
            cursor.execute(sql_insert, (lang['sISOCode'], lang['sName']))
            cursor.execute("SELECT @@IDENTITY AS id;")
            row = cursor.fetchone()
            if row:
                languages_ids.append(row.id)
                print('Linguagem adicionada: ', lang['sName'])
            
        except pyodbc.IntegrityError as e:
            print('Linguagem não adicionada: ', lang['sName'])
            cursor.execute("SELECT id FROM country_info.languages WHERE sCode = ?;", (lang['sISOCode']))
            row = cursor.fetchone()
            if row:
                languages_ids.append(row.id)
            continue
            
    return languages_ids

def ajustar_lang_countries(cursor: pyodbc.Cursor, country_code: str, language_ids: list):
        if len(language_ids) == 0:
            return

        for lang_id in language_ids:
            try:
                sql_insert = "INSERT INTO country_info.lang_countries (CountryID, languageID) VALUES ((SELECT id FROM country_info.countries WHERE sCode = ?), ?);"
                cursor.execute(sql_insert, (country_code, lang_id))
            except pyodbc.IntegrityError as e:
                print(f'Linguagem com id {lang_id} já associada ao país {country_code}.')
                continue


        


    
