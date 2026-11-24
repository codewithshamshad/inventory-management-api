from fastapi import Query

def pagination(skip: int = Query(default=0, ge=0), limit: int = Query(default=10, gt=0,le=100)):
    return {"skip": skip, "limit": limit}