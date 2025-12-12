from zeep import Client, helpers

WSDL_URL = 'http://webservices.oorsprong.org/websamples.countryinfo/CountryInfoService.wso?WSDL'

def iniciar_conexao() -> Client:
    return Client(WSDL_URL)

def get_dados_completos_paises(client, country_iso_code: str) -> dict:
    country = client.service.FullCountryInfo(country_iso_code)
    country_dict = helpers.serialize_object(country, target_cls=dict)

        
    country_response = dict(iso_code=country_dict['sISOCode'], 
                                           name=country_dict['sName'],
                                           phone_code=country_dict['sPhoneCode'],
                                           currency_code=country_dict['sCurrencyISOCode'],
                                           continent_code=country_dict['sContinentCode'],
                                           language_codes=[lang['sISOCode'] for lang in country_dict['Languages']['tLanguage']],
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


def get_dados_linguagens(client, country_languages_codes: str) -> list[dict]:
    languages = client.service.ListOfLanguagesByCode()
    languages_dict = helpers.serialize_object(languages, target_cls=dict)

    total_languages = []
    for language in languages_dict:
        if language['sISOCode'] in country_languages_codes:
            total_languages.append(language)
    return total_languages
        




  