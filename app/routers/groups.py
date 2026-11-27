from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import models
from app.schemas import GroupCreate,GroupView

router = APIRouter()


@router.post("/", response_model=GroupView)
def create_group(
    group: GroupCreate,
    db: Session = Depends(get_db)
):
    normalized_name = group.name.strip().upper()
    if not normalized_name:
        raise HTTPException(status_code=422, detail="Group name cannot be empty")

    existing = db.query(models.Group).filter(
        models.Group.name == normalized_name
    ).first()

    if existing:
        raise HTTPException(
            status_code=409,
            detail="Group already exists"
        )

    new_group = models.Group(name=normalized_name)

    db.add(new_group)
    db.commit()
    db.refresh(new_group)

    return new_group

@router.get("/view",response_model=list[GroupView])
def view_group(db: Session = Depends(get_db)):
    groups = db.query(models.Group).all()
    return groups