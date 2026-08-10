from pydantic import BaseModel, Field
from typing import Optional

class ProductBase(BaseModel):
    name: str
    description: str
    category: str
    price: float = Field(..., ge=0)
    original_price: float = Field(..., ge=0)
    unit: str
    stock: int = Field(..., ge=0)
    image_url: Optional[str] = None
    rating: float = Field(0, ge=0, le=5)

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = Field(None, ge=0)
    original_price: Optional[float] = Field(None, ge=0)
    unit: Optional[str] = None
    stock: Optional[int] = Field(None, ge=0)
    image_url: Optional[str] = None
    rating: Optional[float] = Field(None, ge=0, le=5)

class ProductStockUpdate(BaseModel):
    stock: int = Field(..., ge=0)

class ProductResponse(ProductBase):
    id: str
