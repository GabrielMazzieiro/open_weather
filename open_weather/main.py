from fastapi import FastAPI
from src.db.connections import mongo_client

app = FastAPI()

@app.get("/")
def read_root():
    return {"Status": "Ok"}

@app.post("/create_database")
def create_database():
    mongo_client.teste_db.teste_collection.insert_one({"teste": "teste"})
    return "ok"
