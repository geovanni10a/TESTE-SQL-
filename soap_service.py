from zeep import Client, helpers

WSDL_URL = 'http://webservices.oorsprong.org/websamples.countryinfo/CountryInfoService.wso?WSDL'

# iniciar conexão com o serviço SOAP
def iniciar_conexao() -> Client:
    return Client(WSDL_URL)

# Obter todos os dados de países disponíveis no serviço SOAP
def get_dados_paises(client: Client) -> list:
    full_country = client.service.FullCountryInfoAllCountries()
    full_country_dict = helpers.serialize_object(full_country, target_cls=dict)

    #retorna um array de dicionários com os dados dos países
    full_country_response = [dict(iso_code=country_dict['sISOCode'], 
                            name=country_dict['sName'],
                            capital_city=country_dict['sCapitalCity'],
                            phone_code=country_dict['sPhoneCode'],
                            currency_code=country_dict['sCurrencyISOCode'],
                            continent_code=country_dict['sContinentCode'],
                            languages=country_dict['Languages']['tLanguage'] if country_dict['Languages'] else [],
                            flag=country_dict['sCountryFlag']) for country_dict in full_country_dict]

    return full_country_response

# retorna um array com os dados monetários de todos os países
def get_dados_monetarios(client: Client) -> dict:
    currency = client.service.ListOfCurrenciesByCode()
    currency_dict = helpers.serialize_object(currency, target_cls=dict)
    return currency_dict

# retorna array de dados dos continentes
def get_dados_continentes(client: Client) -> dict:
    continents = client.service.ListOfContinentsByCode()
    continents_dict = helpers.serialize_object(continents, target_cls=dict)

    return continents_dict

# retorna array de dados das línguas
def get_dados_linguas(client: Client) -> dict:
    languages = client.service.ListOfLanguagesByCode()
    languages_dict = helpers.serialize_object(languages, target_cls=dict)

    return languages_dict