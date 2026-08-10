from pydantic import BaseModel, Field
from typing import List

class CartItemBase(BaseModel):
    user_id: str
    product_id: str
    quantity: int = Field(..., gt=0)

class CartItemCreate(CartItemBase):
    pass

class CartItemUpdate(BaseModel):
    quantity: int = Field(..., gt=0)

class CartItemResponse(BaseModel):
    product_id: str
    name: str
    price: float
    quantity: int
    subtotal: float

class CartResponse(BaseModel):
    items: List[CartItemResponse]
    subtotal: float
    delivery_fee: float
    discount: float
    total: float
