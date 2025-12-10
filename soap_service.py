from zeep import Client

WSDL_URL = 'http://webservices.oorsprong.org/websamples.countryinfo/CountryInfoService.wso?WSDL'

def get_dados_continentes() -> list:
    client = Client(wsdl=WSDL_URL)
    continents = client.service.ListOfContinentsByCode()
    return continents



  