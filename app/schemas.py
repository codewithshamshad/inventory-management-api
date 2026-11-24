from pydantic import BaseModel
from enum import StrEnum
from pydantic import ConfigDict

class CategoryCreate(BaseModel):
    name: str


class CategoryView(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)

class Category(StrEnum):
    Electronics = "Electronics"
    Accessories = "Accessories"
    Mouse = "Mouse"
    Safety = "Safety"
    Mobile="Mobile"
    PPE="PPE"

class ItemCreate(BaseModel):
    name: str
    category_id: int
    quantity: int
    price: float


class ItemView(BaseModel):
    id:int
    name: str
    category: CategoryView
    quantity: int
    price: float
    model_config = ConfigDict(from_attributes=True)

class ItemUpdate(BaseModel):
    name: str
    category: Category
    quantity: int
    price : float

class ItemPatch(BaseModel):
    name:str | None = None
    category: Category | None = None
    quantity: int | None = None
    price: float | None = None


class SortBy(StrEnum):
    id = "id"
    name = "name"
    price = "price"
    quantity = "quantity"

class SortOrder(StrEnum):
    asc = "asc"
    desc = "desc"
