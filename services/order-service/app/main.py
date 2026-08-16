import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.config import settings

app = FastAPI(title=settings.service_name)


class OrderRequest(BaseModel):
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


@app.post("/orders")
async def create_order(order: OrderRequest):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{settings.inventory_service_url}/inventory/reserve",
                json={"product_id": order.product_id, "quantity": order.quantity},
                timeout=5.0,
            )
        except httpx.RequestError as exc:
            raise HTTPException(
                status_code=503,
                detail=f"Inventory service unreachable: {exc}",
            )

    if response.status_code == 404:
        raise HTTPException(status_code=404, detail="Product not found")
    if response.status_code == 409:
        raise HTTPException(status_code=409, detail=response.json().get("detail"))
    if response.status_code != 200:
        raise HTTPException(
            status_code=502,
            detail=f"Unexpected response from inventory service: {response.status_code}",
        )

    reservation = response.json()
    return {
        "order_status": "confirmed",
        "product_id": order.product_id,
        "quantity": order.quantity,
        "inventory_remaining": reservation["remaining_stock"],
    }