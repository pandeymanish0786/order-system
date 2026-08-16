from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.config import settings

app = FastAPI(title=settings.service_name)

# Temporary in-memory "database" — a plain dict standing in for Postgres for now.
# Keys are product_id, values are available stock count.
inventory_db = {
    "product-1": 10,
    "product-2": 5,
    "product-3": 0,
}


class ReserveRequest(BaseModel):
    product_id: str
    quantity: int


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": settings.service_name,
        "environment": settings.environment,
    }


@app.get("/")
def root():
    return {"message": f"{settings.service_name} is running"}


@app.get("/inventory/{product_id}")
def get_stock(product_id: str):
    if product_id not in inventory_db:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"product_id": product_id, "available_stock": inventory_db[product_id]}


@app.post("/inventory/reserve")
def reserve_stock(req: ReserveRequest):
    if req.product_id not in inventory_db:
        raise HTTPException(status_code=404, detail="Product not found")

    available = inventory_db[req.product_id]
    if available < req.quantity:
        raise HTTPException(
            status_code=409,
            detail=f"Insufficient stock: requested {req.quantity}, available {available}",
        )

    inventory_db[req.product_id] -= req.quantity
    return {
        "product_id": req.product_id,
        "reserved": req.quantity,
        "remaining_stock": inventory_db[req.product_id],
    }