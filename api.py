from fastapi import FastAPI, Path,HTTPException
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):

    name:str
    price:float
    brand: Optional[str] = None

class UpdateItem(BaseModel):

    name: Optional[str] = None
    price: Optional[float] = None
    brand: Optional[str] = None

inventory = {}


@app.get("/item/{id}")
async def root(id: int = Path(description="the id of the item")):
    return inventory[id]

# there are two types of parametres path(/) and query(?)  
#  * the asterix could be added in def item(here) to solve agument problems
@app.get("/get-by-name") 
def get_item(name : Optional[str] = None):
    for item_id in inventory:
        if inventory[item_id].name == name:
            return inventory[item_id]
        raise HTTPException(status_code=404)
       
    
@app.post("/create-item/{item_id}")
def create_item(item_id : int ,item : Item):
    if item_id in inventory:
        return {"error":"item id already exists"}
    inventory[item_id] = item
    return inventory[item_id]

@app.put("/update-item/{item_id}")
def update_item(item_id : int , item : UpdateItem):
    if item_id not in inventory:
        return {"Error" : "Item doesn't exist"}
    
    if item.name != None:
        inventory[item_id].name = item.name
    if item.price != None:
        inventory[item_id].price = item.price
    if item.brand != None:
        inventory[item_id].brand = item.brand
    return  inventory[item_id]

@app.delete("/delete-item/{item_id}")
def delete_item(item_id : int):
    if item_id not in inventory:
        return {"error":"Item doesn't exist"}
    del inventory[item_id]
    return {"success" : "item deleted"}

