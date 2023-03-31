# import requests_async as requests
import requests 
import traceback
from os import getenv


API_KEY = getenv('OPEN_WEATHER_API_KEY')
OW_URL_5_DIAS = getenv('OW_URL_5_DIAS')
OW_URL_GEO = getenv('OW_URL_GEO')

async def get_open_weather_data(lat: str | None=None, lon: str | None=None, city_name='Belo Horizonte', country_code="BRA", units="metric"):
    '''
    Function to handle api request to openweathermap.org. 
    If lat=None or lon=None, city_name and country_code will be used

    @params: lat -> Latitude | str
    @params: lon -> Longitude | str
    @params: city_name -> name of the city you want do check
    @params: country_code -> country code of the city you want do check, ISO 3166 
    @params: units -> metric (Celsius) or imperial (Fehrenheit) | str

    Return: 
    Api response
    '''
    
    try:
        # TODO: implementar logica para aceitar limit como parametro e retornar mais opções

        # Se recebemos Lat e long não precisamos buscar por cidade e país
        if not lat and not lon:

            # Recupera o dado de local, lat e long do openweather para usar na busca
            geo_response = requests.get(f'{OW_URL_GEO}?q={city_name},{country_code}&limit=1&appid={API_KEY}')
            
            #confere se retornou 200
            assert geo_response.status_code == 200, 'Tivemos problemas para recuperar as informações de lat e lon dessa localidade'

            geo_response = geo_response.json()

            # Se chegou aqui, recupera o lat e lon retornado
            lat = geo_response[0]['lat']
            lon = geo_response[0]['lon']
        

        weather_response = requests.get(f'{OW_URL_5_DIAS}?lat={lat}&lon={lon}&appid={API_KEY}&units={units}')
        
        assert weather_response.status_code == 200, 'O tempo deve estar bem ruim mesmo, não conseguimos sua previsão.'

        return weather_response.json()

    except Exception as exp:
        traceback.print_exc(exp)

