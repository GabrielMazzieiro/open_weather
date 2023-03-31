from fastapi import FastAPI
from src.db.connections import mongo_client
from src.api.routes import api_router

app = FastAPI()
app.include_router(api_router)

@app.get("/")
def read_root():
    return {"Status": "Ok",
            "Message": "access localhost:8000/docs to see all endpoints"}

