from pydantic import BaseModel
from typing import List
from datetime import datetime
from app.schemas.cart import CartItemResponse

class OrderCreate(BaseModel):
    user_id: str
    delivery_address: str
    payment_method: str = "COD"

class OrderStatusUpdate(BaseModel):
    status: str # pending, confirmed, packed, out_for_delivery, delivered, cancelled

class OrderResponse(BaseModel):
    id: str
    user_id: str
    items: List[CartItemResponse]
    subtotal: float
    delivery_fee: float
    total: float
    delivery_address: str
    payment_method: str
    status: str
    created_at: datetime
