from zeep import Client, helpers

WSDL_URL = 'http://webservices.oorsprong.org/websamples.countryinfo/CountryInfoService.wso?WSDL'

def iniciar_conexao() -> Client:
    return Client(WSDL_URL)

def get_codigos_paises(client: Client) -> list:
    countries = client.service.ListOfCountryNamesByCode()
    countries_dict = helpers.serialize_object(countries, target_cls=dict)
    
    country_codes = [country['sISOCode'] for country in countries_dict]
    return country_codes

# Verifica se o país está disponível no serviço SOAP
# A ser usada se necessário
def is_pais_disponivel(client: Client, country_iso_code: str) -> bool:
    countries = client.service.ListOfCountryNamesByCode()
    countries_dict = helpers.serialize_object(countries, target_cls=dict)

    for country in countries_dict:
        if country['sISOCode'] == country_iso_code:
            return True
    return False

def get_dados_completos_paises(client, country_iso_code: str) -> dict:
    country = client.service.FullCountryInfo(country_iso_code)
    country_dict = helpers.serialize_object(country, target_cls=dict)

    country_response = dict(iso_code=country_dict['sISOCode'], 
                            name=country_dict['sName'],
                            capital_city=country_dict['sCapitalCity'],
                            phone_code=country_dict['sPhoneCode'],
                            continent_code=country_dict['sContinentCode'],
                            languages=country_dict['Languages']['tLanguage'] if country_dict['Languages'] else [],
                            flag=country_dict['sCountryFlag'])

    return country_response
    
def get_dados_monetarios(client, country_iso_code: str) -> dict:
    currency = client.service.CountryCurrency(country_iso_code)
    currency_dict = helpers.serialize_object(currency, target_cls=dict)
    return currency_dict

def get_dados_continente(client, continent_iso_code: str) -> dict:
    continents = client.service.ListOfContinentsByCode()
    continents_dict = helpers.serialize_object(continents, target_cls=dict)

    for continent in continents_dict:
        if continent['sCode'] == continent_iso_code:
            return continent


        




  