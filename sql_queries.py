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

# insere dados de todos os continentes
def inserir_dados_continente(cursor, all_continent_data: dict) -> int:
    sql_insert = "INSERT INTO country_info.continents (sCode, sName) VALUES (?, ?);"

    for continent_data in all_continent_data:
        try:
            cursor.execute(sql_insert, (continent_data['sCode'], continent_data['sName']))

            cursor.execute("SELECT id FROM country_info.continents WHERE sCode = ?", (continent_data['sCode']))

            print('Continente adicionado: ', continent_data['sName'])
        except pyodbc.IntegrityError:
            cursor.execute("SELECT id FROM country_info.continents WHERE sCode = ?", (continent_data['sCode']))

# insere dados de todas as moedas
def inserir_dados_monetarios(cursor, all_currency_data: dict) -> int:
    sql_insert = "INSERT INTO country_info.currencies (sCode, sName) VALUES (?, ?);"

    for currency_data in all_currency_data:
        try:
            cursor.execute(sql_insert, (currency_data['sISOCode'], currency_data['sName']))

            print('Moeda adicionada: ', currency_data['sName'])
        except pyodbc.IntegrityError:
            cursor.execute("SELECT id FROM country_info.currencies WHERE sCode = ?", (currency_data['sISOCode']))

# insere dados de todas as linguagens
def inserir_dados_linguagens(cursor, all_language_data: dict) -> list:
    sql_insert = "INSERT INTO country_info.languages (sCode, sName) VALUES (?, ?);"
    language_ids = []

    for language_data in all_language_data:
        try:
            cursor.execute(sql_insert, (language_data['sISOCode'], language_data['sName']))

            print('Língua adicionada: ', language_data['sName'])
        except pyodbc.IntegrityError:
            cursor.execute("SELECT id FROM country_info.languages WHERE sCode = ?", (language_data['sISOCode'],))

    return language_ids

# insere dados de todos os países
def inserir_dados_paises(cursor, all_country_data: dict):
    for country_data in all_country_data:
        fk_continent = None
        fk_currency = None

        # obtém fk_continent
        cursor.execute("SELECT id FROM country_info.continents WHERE sCode = ?", (country_data['continent_code'],))
        row = cursor.fetchone()
        if row:
            fk_continent = row.id

        # obtém fk_currency
        cursor.execute("SELECT id FROM country_info.currencies WHERE sCode = ?", (country_data['currency_code'],))
        row = cursor.fetchone()
        if row:
            fk_currency = row.id

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
        except pyodbc.IntegrityError:
            print('País não adicionado: ', country_data['name'])

# ajusta tabela joint lang_countries
def ajustar_lang_countries(cursor, all_country_data):
    for country in all_country_data:

        country_id = None
        language_id = None

        cursor.execute("SELECT id FROM country_info.countries WHERE sCode = ?;", (country['iso_code']))
        row = cursor.fetchone()
        if row:
            country_id = row.id

        for lang in country['languages']:

            cursor.execute("SELECT id FROM country_info.languages WHERE sCode = ?;", (lang['sISOCode']))
            row = cursor.fetchone()
            if row:
                language_id = row.id
            
            try:
                cursor.execute("INSERT INTO country_info.lang_countries (fkCountry, fkLanguage) VALUES (?, ?);",
                                (country_id, language_id))
                print(f"Língua {lang['sName']} associada ao país {country['name']}")
            except pyodbc.IntegrityError:
                print(f"Língua {lang['sName']} já associada ao país {country['name']}")

def inserir_dados(cursor, /, full_continent_data, full_language_data, full_currency_data, full_countries_data):
    inserir_dados_continente(cursor, full_continent_data)
    inserir_dados_monetarios(cursor, full_currency_data)
    inserir_dados_linguagens(cursor, full_language_data)

    inserir_dados_paises(cursor, full_countries_data)
    ajustar_lang_countries(cursor, full_countries_data)