from pydantic import BaseModel
from fastapi import FastAPI,Query,HTTPException,status,Response, Depends
from enum import StrEnum
from database import engine,Base ,SessionLocal,get_db
import models
from sqlalchemy import text, select
from sqlalchemy.orm import Session

app = FastAPI()
Base.metadata.create_all(engine)

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


class SortBy(StrEnum):
    id = "id"
    name = "name"
    price = "price"
    quantity = "quantity"

class SortOrder(StrEnum):
    asc = "asc"
    desc = "desc"

def pagination(skip: int = Query(default=0, ge=0), limit: int = Query(default=10, gt=0)):
    return {"skip": skip, "limit": limit}


@app.get("/")
def home():
    return {"message": "Welcome to Inventory Management API"}


@app.get("/items", response_model=list[ItemView])
def get_items(
    category: Category | None = None,
    search: str | None = None,
    sort_by: SortBy = SortBy.id,
    order: SortOrder = SortOrder.asc,
    data=Depends(pagination),
    db: Session = Depends(get_db),
):
    skip = data["skip"]
    limit = data["limit"]

    stmt = select(models.Item)

    # Filter by category
    if category:
        stmt = stmt.where(
            models.Item.category == category
        )

    # Search by name
    if search:
        stmt = stmt.where(
            models.Item.name.ilike(f"%{search}%")
        )

    # Sorting
    sort_column = getattr(
        models.Item,
        sort_by.value
    )

    if order == SortOrder.desc:
        stmt = stmt.order_by(
            sort_column.desc()
        )
    else:
        stmt = stmt.order_by(
            sort_column.asc()
        )

    # Pagination
    stmt = stmt.offset(skip).limit(limit)

    result = db.execute(stmt)

    return result.scalars().all()

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

@app.patch("/items/{item_id}", response_model=ItemView)
def patch_item(
    item_id: int,
    updated_item: ItemPatch,
    db: Session = Depends(get_db)
):
    item = db.get(models.Item, item_id)

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )

    updated_data = updated_item.model_dump(
        exclude_unset=True
    )

    for field, value in updated_data.items():
        setattr(item, field, value)

    db.commit()
    db.refresh(item)

    return item

@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(
    item_id: int,
    db: Session = Depends(get_db)
):
    stmt = select(models.Item).where(
        models.Item.id == item_id
    )

    item = db.execute(stmt).scalar_one_or_none()

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )

    db.delete(item)
    db.commit()

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )
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