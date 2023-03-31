from fastapi import APIRouter, HTTPException
from .open_weather import get_open_weather_data
from ..utils.formater import format_api_response
from src.db.connections import mongo_client
import traceback
from copy import deepcopy as copy

api_router = APIRouter(prefix='/api')

@api_router.get("/get_forecast")
async def get_forecast(city_name: str, country_code: str, units: str,  lat: str | None = None, lon: str | None = None):
    
    try:
        
        weather_response = await get_open_weather_data(
                                            lat=lat,
                                            lon=lon, 
                                            city_name=city_name, 
                                            country_code=country_code,
                                            units=units, 
    )

        formatted_response = format_api_response(weather_response)

        final_data = copy(formatted_response)

        mongo_client.open_weather.forecast.insert_one(formatted_response)

        return final_data
    
    except Exception as exp:
        tb_str = ''.join(traceback.format_exception(None, exp, exp.__traceback__, chain=True))
        raise HTTPException(400, detail=tb_str)


@api_router.get("/check_day")
async def check_day(day: str, city: str):
    try:

        print(day)

        last_data = mongo_client.open_weather.forecast.find_one({
            day: {'$exists': True}, 
            'city': city
            })
        
        assert last_data, "Infelizmente não temos dados dessa cidade para esse dia, tente acessar o endereço /api/get_forecast para recuperarmos"

        final_data = {
            "city": last_data['city'],
            'country':last_data['country'],
            'insert_datetime_int_utc':last_data['insert_datetime_int_utc'],
            'insert_datetime_str_utc':last_data['insert_datetime_str_utc'],
            day: last_data[day]
        }

        message = ("Esse é o dado mais atual que temos no banco para o dia buscado. \
                    Se precisar de um dado mais novo, acesse o endereço /api/get_forecast para recuperarmos um dado novo")

        return message, final_data


    except AssertionError as ass:
        print(ass)
        return {'message': "Infelizmente não temos dados dessa cidade para esse dia, tente acessar o endereço /api/get_forecast para recuperarmos"}

    except Exception as exp:
        tb_str = ''.join(traceback.format_exception(None, exp, exp.__traceback__, chain=True))
        raise HTTPException(400, detail=tb_str)

