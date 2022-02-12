from calendar import c
from cgitb import reset
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
    timestampin: Optional[int] = 0
    timestampinn: Optional[int] = 0
    timestampout: Optional[int] = 0
    sum_time: Optional[int] = 0
    cnt: Optional[int] = 0

client = MongoClient('mongodb://localhost', 27017)

db = client["Toilet"]
collection = db["data"]

app = FastAPI()
   
@app.put("/toilet/update")
def func(toilet: Toilet):
    query = {"room": toilet.room}
    result = collection.find_one(query)
    LED_status = {"$set":{"status":toilet.status}}
    Toilet.update_one(query,LED_status)
    #print(result['status'])
    if (result['status'] == 1 and toilet.cnt == 0): #0=เข้า
        if (toilet.status == 0):
            inn = datetime.now()
            toilet.timestampin = datetime.timestamp(inn)
            return {
                "room": toilet.room,
                "status": toilet.status,
                "time_in": f"{datetime.fromtimestamp(toilet.timestampin).hour}:{datetime.fromtimestamp(toilet.timestampin).minute}"
            }
        
    elif (result['status'] == 1):
        if (toilet.status == 0):
            inn = datetime.now()
            toilet.timestampin = datetime.timestamp(inn)
            return {
                "room": toilet.room,
                "status": toilet.status,
                "time_in": f"{datetime.fromtimestamp(toilet.timestampin).hour}:{datetime.fromtimestamp(toilet.timestampin).minute}"
            }
    elif(result['status'] == 0):
        if (toilet.status == 1):
            out = datetime.now()
            toilet.timestampout = datetime.timestamp(out)
            toilet.sum_time += (toilet.timestampout-toilet.timestampin)
            toilet.cnt = toilet.cnt+1
            return {
                "room": toilet.room,
                "status": toilet.status,
                "time_in": f"{datetime.fromtimestamp(toilet.timestampin).hour}:{datetime.fromtimestamp(toilet.timestampin).minute}"
            }
        elif (result['status'] == 0):
            inn = datetime.now()
            toilet.timestampinn = datetime.timestamp(inn) - toilet.timestampin
            return {
                "room": toilet.room,
                "status": toilet.status,
                "time_in": f"{datetime.fromtimestamp(toilet.timestampin).hour}:{datetime.fromtimestamp(toilet.timestampin).minute}",
                "duration": toilet.timestampinn
            }
    
@app.get("/toilets") 
def time_estimate(toilet: Toilet):
    sum = 0
    sum_time = 0
    query = {"room": toilet.room}
    for x in collection.find():
        sum += x['cnt']
    #print(sum) 
    return {
        "room" : toilet.room,
        "status": toilet.status,
        "time_in": f"{datetime.fromtimestamp(toilet.timestampin).hour}:{datetime.fromtimestamp(toilet.timestampin).minute}",
        "duration": toilet.timestampinn,
        "cnt": toilet.cnt,
        "estimate": toilet.sum_time/sum
    }