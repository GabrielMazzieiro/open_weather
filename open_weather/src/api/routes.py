from fastapi import APIRouter, HTTPException
from .open_weather import get_open_weather_data
from ..utils.formater import format_api_response
from src.db.connections import mongo_client
import traceback

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

        mongo_client.open_weather.forecast.insert_one(formatted_response)

        return formatted_response
    
    except Exception as exp:
        raise HTTPException(400, detail=str(traceback.print_exc(exp)))



