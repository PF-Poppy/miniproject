from fastapi import FastAPI
from pymongo import MongoClient
from pydantic import BaseModel



class Toilet(BaseModel):
    room: int
    # Led: int
    in_time_hour: int
    in_time_minutes: int
    out_time_hour: int
    out_time_minutes: int
    
client = MongoClient('mongodb://localhost', 27017)

db = client["Toilet"]

collection = db["data"]

app = FastAPI()

@app.post("/toilet")
def reserve(reservation : Toilet):
    pass

@app.put("/toilet/update/")
def update_reservation(reservation: Toilet):
    pass

