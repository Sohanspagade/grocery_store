from pydantic import BaseModel, Field
from typing import List, Optional

class ChatRequest(BaseModel):
    user_id: str
    message: str

class ChatResponse(BaseModel):
    message: str
    conversation_id: str

class ShoppingListRequest(BaseModel):
    people: int = Field(..., gt=0)
    days: int = Field(..., gt=0)
    budget: float = Field(..., gt=0)
    diet: str
    requirements: Optional[str] = None

class ShoppingListItem(BaseModel):
    product_id: str
    name: str
    quantity: int
    unit: str
    price: float

class ShoppingListResponse(BaseModel):
    shopping_list: List[ShoppingListItem]
    estimated_total: float

class RecommendationsRequest(BaseModel):
    user_id: str

class SearchRequest(BaseModel):
    query: str
