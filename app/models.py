from sqlalchemy import String, Integer, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column,relationship
from app.database import Base
from typing import List


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)

    items: Mapped[List["Item"]] = relationship(
        back_populates="category"
    )


class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer)
    price: Mapped[float] = mapped_column(Float)
    sku: Mapped[str] = mapped_column(String(100))
    description : Mapped[str] = mapped_column(String(500))

    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id")
    )
    group_id: Mapped[int] = mapped_column(
        ForeignKey("groups.id")
    )

    # relationships
    category: Mapped["Category"] = relationship(back_populates="items")
    group: Mapped["Group"] = relationship(back_populates="items")

class Group(Base):
    __tablename__ = "groups"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    items: Mapped[List["Item"]] = relationship(back_populates="group")

