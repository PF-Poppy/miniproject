from calendar import c
from xmlrpc import client
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from fastapi.encoders import jsonable_encoder

from pymongo import MongoClient

app = FastAPI()

client = MongoClient('mongodb://localhost', 27017)

db = client["teach"]
menu_collection = db["menu"]

class Menu(BaseModel):
    name: str
    price: int
    amount: int  
    
@app.post("/new-menu")
def add_menu(menu: Menu):
    m = jsonable_encoder(menu)
    print(m)
    menu_collection.insert_one(m)
    
@app.get("/menu/{name}")
def get_menu(name: str):
    result = menu_collection.find_one({"name": name}, {"_id":0})
    print(result)
    if result != None:
        return {
            "status": "found",
            "result": result
        }
    else:
        raise HTTPException(404, f"Couldn't find menu with name: {name}'")