from fastapi import FastAPI
from pymongo import MongoClient

app = FastAPI()

client = MongoClient('mongodb://localhost', 27017)
db = client["teach"]
menu_collection = db["menu"]

@app.get("/fruit/all")
def get_all_fruit():
    result = menu_collection.find({}, {"_id": 0, "name": 1})
    my_result = []
    for r in result:
        my_result.append(r)
    print(my_result)
    return {
        "result": my_result
    }
    
@app.post("/fruit/add/{name}/{price}")
def add_new_fruit(name: str, price: int):
    new_fruit = {
        "name": name,
        "price": price
    }
    menu_collection.insert_one(new_fruit)
    return {
        "result": "done",
    }
    
@app.delete("/fruit/del/{name}")
def remove_one_fruit(name: str):
    query = {"name": name}
    menu_collection.delete_one(query)
    return {
        "result": "done",
    }
    
@app.put("/fruit/update/{name}/{new_price}")
def update_price(name: str, new_price: int):
    query = {"name": name}
    new_values = { "$set": {"price": new_price}}
    menu_collection.update_one(query, new_values)