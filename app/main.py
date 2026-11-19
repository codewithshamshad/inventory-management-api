from pydantic import BaseModel
from fastapi import FastAPI,Query,HTTPException
from enum import StrEnum

app = FastAPI()

items = [
    {
        "id": 1,
        "name": "Laptop",
        "category": "Electronics",
        "quantity": 15,
        "price": 3500
    },
    {
        "id": 2,
        "name": "Keyboard",
        "category": "Accessories",
        "quantity": 25,
        "price": 150
    },
    {
        "id": 3,
        "name": "Mouse",
        "category": "Accessories",
        "quantity": 30,
        "price": 80
    },
    {
        "id": 4,
        "name": "Safety Gloves",
        "category": "Safety",
        "quantity": 100,
        "price": 25
    },
    {
        "id": 5,
        "name": "Hard Hat",
        "category": "Safety",
        "quantity": 50,
        "price": 60
    },
    {
        "id": 6,
        "name": "Hp12 Mouse",
        "category": "Mouse",
        "quantity": 50,
        "price": 60
    }
]
class Category(StrEnum):
    Electronics = "Electronics"
    Accessories = "Accessories"
    Mouse = "Mouse"
    Safety = "Safety"
    Mobile="Mobile"

class ItemCreate(BaseModel):
    id:int
    name: str
    category: Category
    quantity: int
    price: float


class ItemView(BaseModel):
    id:int
    name: str
    category: str
    quantity: int

@app.get("/")
def home():
    return {"message": "Welcome to Inventory Management API"}

@app.get("/items",response_model=list[ItemView])
def get_items(category:Category|None=None,skip:int=Query(default=0,ge=0),limit:int=Query(default=10,gt=0)):
    if category:
        # filter item by category
        filter_item=[item for item in items if item["category"] == category]
        return filter_item[skip:skip+limit]
    # get all items with limit parameter
    return items[skip:skip+limit]

@app.get("/items/{item_id}",response_model=ItemView)
def get_item_by_id(item_id:  int):
    for item in items:
        if item["id"] == item_id:
            return item
    else:
        raise HTTPException(status_code=404, detail="Item not found")

@app.post("/items",response_model=ItemView)
def create_item(item: ItemCreate):
    items.append(item.model_dump())
    return item
