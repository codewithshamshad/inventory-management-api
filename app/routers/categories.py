from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import models
from app.schemas import CategoryCreate, CategoryView

router = APIRouter()


@router.post("/", response_model=CategoryView)
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db)
):
    existing = db.query(models.Category).filter(
        models.Category.name == category.name
    ).first()

    if existing:
        raise HTTPException(
            status_code=409,
            detail="Category already exists"
        )

    new_category = models.Category(name=category.name.strip().upper())

    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category

@router.get("/view",response_model=list[CategoryView])
def view_category(db: Session = Depends(get_db)):
    categories = db.query(models.Category).all()
    return categories