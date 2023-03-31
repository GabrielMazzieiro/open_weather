from fastapi import APIRouter, HTTPException
from .open_weather import get_open_weather_data
from ..utils.formater import format_api_response
from src.db.connections import mongo_client
import traceback
from copy import deepcopy as copy

api_router = APIRouter(prefix='/api')

@api_router.get("/forecast")
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



