from pydantic import BaseModel
from fastapi import FastAPI,Query,HTTPException,status,Response, Depends
from enum import StrEnum
from database import engine,Base ,SessionLocal,get_db
import models
from sqlalchemy import text
from sqlalchemy.orm import Session

app = FastAPI()
Base.metadata.create_all(engine)
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
    PPE="PPE"

class ItemCreate(BaseModel):
    name: str
    category: Category
    quantity: int
    price: float


class ItemView(BaseModel):
    id:int
    name: str
    category: Category
    quantity: int

class ItemUpdate(BaseModel):
    name: str
    category: Category
    quantity: int
    Price : float
class ItemPatch(BaseModel):
    name:str | None = None
    category: Category | None = None
    quantity: int | None = None
    price: int | None = None


def pagination(skip: int = Query(default=0, ge=0), limit: int = Query(default=10, gt=0)):
    return {"skip": skip, "limit": limit}


@app.get("/")
def home():
    return {"message": "Welcome to Inventory Management API"}


@app.get("/items", response_model=list[ItemView])
def get_items(
    category: Category | None = None,
    data=Depends(pagination),
    db: Session = Depends(get_db)
):
    skip = data["skip"]
    limit = data["limit"]

    query = db.query(models.Item)

    if category:
        query = query.filter(
            models.Item.category == category
        )

    items = query.offset(skip).limit(limit).all()

    return items


@app.get("/items/{item_id}",response_model=ItemView)
def get_item_by_id(item_id:  int,db: Session = Depends(get_db)):
    item=(db.query(models.Item).filter(models.Item.id == item_id).first())

    if item is None:
        raise HTTPException(status_code=404,detail="Item not Found")
    return item



@app.put("/items/{item_id}", response_model=ItemView)
def update_item(
    item_id: int,
    updated_item: ItemUpdate,
    db: Session = Depends(get_db)
):
    item = db.query(models.Item).filter(
        models.Item.id == item_id
    ).first()

    if item is None:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )

    for key, value in updated_item.model_dump().items():
        setattr(item, key, value)

    db.commit()
    db.refresh(item)

    return item

@app.patch("/items/{item_id}")
def patch_tem(item_id:int,updated_item: ItemPatch):
    for item in items:
        if item["id"] == item_id:
            updated_data=updated_item.model_dump(exclude_unset=True)
            print(updated_data)
            item.update(updated_data)
            return item

    raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/items/{item_id}")
def delete_item(item_id:int):
    item_to_delete = None
    for item in items:
        if item["id"] == item_id:
            item_to_delete = item
            break
    if item_to_delete is not None:
        items.remove(item_to_delete)
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail="Item not found")

@app.get("/db")
def check_db():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        return {"database": "connected", "result": result.scalar()}


@app.get("/read_databse")
def read_databse():
    db=SessionLocal()
    all_items=db.query(models.Item).all()
    db.close()
    return all_items

@app.post("/create_item")
def create_item(item: ItemCreate):
    db = SessionLocal()

    try:
        # Check if item already exists
        existing_item = (
            db.query(models.Item)
            .filter(models.Item.name == item.name)
            .first()
        )

        if existing_item:
            return {"message": "Item already added"}

        db_item = models.Item(
            name=item.name,
            category=item.category,
            quantity=item.quantity,
            price=item.price
        )

        db.add(db_item)
        db.commit()
        db.refresh(db_item)

        return {
            "message": "Item created successfully",
            "item": db_item
        }

    finally:
        db.close()