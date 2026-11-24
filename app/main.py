from fastapi import FastAPI
from app.database import engine,Base
from app.routers import items, categories

app = FastAPI()
Base.metadata.create_all(engine)

app.include_router(items.router,prefix="/items", tags=["Items"])
app.include_router(categories.router,prefix="/categories", tags=["Categories"])
@app.get("/")
def home():
    return {"message": "Welcome to Inventory Management API"}