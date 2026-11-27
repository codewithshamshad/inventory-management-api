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

class SKU(StrEnum):
    pcs="PCS"
    ea="EA"
    dozen="DOZEN"
    kg="KG"

# class Group(StrEnum):
#     group_a="Group A"
#     group_b="Group B"
#     group_c="Group C"

class GroupCreate(BaseModel):
    name: str
    # model_config = ConfigDict(from_attributes=True)

class GroupView(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)

class ItemCreate(BaseModel):
    name: str
    quantity: int
    price: float
    sku:SKU
    description: str
    category_id: int
    group_id:int
    model_config = ConfigDict(from_attributes=True)


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
