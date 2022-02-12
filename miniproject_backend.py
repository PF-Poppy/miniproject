from calendar import c
from re import T
from this import d
from xmlrpc import client
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from fastapi.encoders import jsonable_encoder
from datetime import datetime
from pymongo import MongoClient

class Toilet(BaseModel):
    room     : int
    status   : int
    cnt: Optional[int] = 0 
    timestampin: Optional[int] = 0
    timestampinn: Optional[int] = 0
    timestampout: Optional[int] = 0
    

client = MongoClient('mongodb://localhost', 27017)

db = client["Toilet"]
collection = db["data"]

app = FastAPI()

@app.post("/toilet")
def add_Information(toilet : Toilet):
    r = jsonable_encoder(toilet)
    collection.insert_one(r)
   
@app.put("/toilet/update/")
def func(toilet: Toilet):
    r = jsonable_encoder(toilet)
    query = {"room": toilet.room}
    if (toilet.status == 1 and toilet.cnt == 0): #0=เข้า
        LED_status = {"$set":{"status":toilet.status}}
        if (LED_status == 0):
            inn = datetime.now()
            toilet.timestampin = datetime.timestamp(inn)
            return {
                "room": toilet.room,
                "status": toilet.status,
                "time_in": f"{toilet.timestampin.hour}:{toilet.timestampin.minute}"
            }
    elif (toilet.status == 1):
        LED_status = {"$set":{"status":toilet.status}}
        if (LED_status == 0):
            inn = datetime.now()
            toilet.timestampin = datetime.timestamp(inn)
            return {
                "room": toilet.room,
                "status": toilet.status,
                "time_in": f"{toilet.timestampin.hour}:{toilet.timestampin.minute}"
            }
    elif(toilet.status == 0):
        LED_status = {"$set":{"status":toilet.status}}
        if (LED_status == 1):
            out = datetime.now()
            toilet.timestampout = datetime.timestamp(out)
            toilet.cnt = toilet.cnt + 1
            return {
                "room": toilet.room,
                "status": toilet.status,
                "time_in": f"{toilet.timestampin.hour}:{toilet.timestampin.minute}",
                "estimated time": (toilet.timestampout-toilet.timestampin)/toilet.cnt
            }
        elif (LED_status == 0):
            inn = datetime.now()
            toilet.timestampinn = datetime.timestamp(inn) - toilet.timestampin
            return {
                "room": toilet.room,
                "status": toilet.status,
                "time_in": f"{toilet.timestampin.hour}:{toilet.timestampin.minute}",
                "duration": toilet.timestampinn
            }
    
@app.get("/toilet/estimate_time/{room}") 
def time_estimate(room: int, toilet: Toilet):
    time_in = datetime.fromtimestamp(toilet.timestampin)
    return {
        "room": toilet.room,
        "status": toilet.status,
        "Time_in": f"{time_in.hour}:{time_in.minute}",
    }

