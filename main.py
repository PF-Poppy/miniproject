from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    discount: Optional[float] = 0

@app.get("/") 
def root():
    return {"Hello": "Exceed"}

@app.post("/")
def root_post():
    return {"Hello": "Exceed from POST"}

@app.put("/")
def root_put():
    return {"Hello": "Exceed from PUT"}

@app.delete("/")
def root_delete():
    return {"Hello": "Exceed from DELETE"}

@app.get("/items/{item_id}")
def get_item(item_id: int, q: Optional[str] = None):
    return {
        "Hello": item_id,"from GET": q}

#@app.post("/items/{item_id}")
#def post_item(item_id: int, q: Optional[str] = None):
#    return {
#        "Hello": item_id,"from POST": q}

@app.put("/items/{item_id}")
def put_item(item_id: int, q: Optional[str] = None):
    return {
        "Hello": item_id,"from PUT": q}

@app.delete("/items/{item_id}")
def delete_item(item_id: int, q: Optional[str] = None):
    return {
        "Hello": item_id,"from DELETE": q}

@app.post("/items/{item_id}")
def get_item(item_id: int, item: Item):
    return {
        "name": item.name, 
        "price": item.price,
        "discount": item.discount}