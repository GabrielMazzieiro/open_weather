from fastapi import FastAPI
from src.db.connections import mongo_client
from open_weather.open_weather.src.api.routes import api_router

app = FastAPI()
app.include_router(api_router)

@app.get("/")
def read_root():
    return {"Status": "Ok"}

@app.post("/create_database")
def create_database():
    mongo_client.teste_db.teste_collection.insert_one({"teste": "teste"})
    return "ok"
