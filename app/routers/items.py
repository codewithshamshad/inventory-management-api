from fastapi import APIRouter, Depends, HTTPException, status,Response
from sqlalchemy import select, text

from app.schemas import (
    ItemPatch,
    ItemCreate,
    ItemUpdate,
    ItemView,
    Category,
    CategoryCreate,
    CategoryView,
    SortBy,
    SortOrder
)

from app.database import SessionLocal, engine, get_db
from sqlalchemy.orm import Session
from app.dependencies import pagination
from app import models

router=APIRouter()

@router.get("/items", response_model=list[ItemView])
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



@router.get("/items/{item_id}",response_model=ItemView)
def get_item_by_id(item_id:  int,db: Session = Depends(get_db)):
    item=(db.query(models.Item).filter(models.Item.id == item_id).first())

    if item is None:
        raise HTTPException(status_code=404,detail="Item not Found")
    return item



@router.put("/items/{item_id}", response_model=ItemView)
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

@router.patch("/items/{item_id}", response_model=ItemView)
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

@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
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
@router.get("/db")
def check_db():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        return {"database": "connected", "result": result.scalar()}


@router.post("/create_item", status_code=status.HTTP_201_CREATED)
def create_item(item: ItemCreate,db:Session=Depends(get_db)):

    # Check if item already exists
    existing_item = (
        db.query(models.Item)
        .filter(models.Item.name == item.name)
        .first()
    )

    if existing_item:
        raise HTTPException(status_code=409, detail="Item already exists")

    db_item = models.Item(
        name=item.name,
        category_id=item.category_id,
        quantity=item.quantity,
        price=item.price,
        sku=item.sku,
        description=item.description,
        group_id=item.group_id
    )

    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    return {
        "message": "Item created successfully",
        "item": db_item
    }

