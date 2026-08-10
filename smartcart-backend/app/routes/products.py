from fastapi import APIRouter, HTTPException, Query, status
from typing import List, Optional
from bson import ObjectId
from app.schemas.product import ProductCreate, ProductUpdate, ProductStockUpdate, ProductResponse
from app.database.mongodb import mongodb

router = APIRouter()

@router.post("/", response_model=ProductResponse)
def create_product(product: ProductCreate):
    collection = mongodb.get_collection("products")
    p_dict = product.model_dump()
    result = collection.insert_one(p_dict)
    return {**p_dict, "id": str(result.inserted_id)}

@router.get("/", response_model=List[ProductResponse])
def get_products(
    page: int = 1,
    limit: int = 20,
    search: Optional[str] = None,
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    sort: Optional[str] = None
):
    collection = mongodb.get_collection("products")
    query = {}
    
    if search:
        query["$or"] = [
            {"name": {"$regex": search, "$options": "i"}},
            {"description": {"$regex": search, "$options": "i"}},
            {"category": {"$regex": search, "$options": "i"}}
        ]
        
    if category:
        query["category"] = {"$regex": f"^{category}$", "$options": "i"}
        
    if min_price is not None or max_price is not None:
        query["price"] = {}
        if min_price is not None:
            query["price"]["$gte"] = min_price
        if max_price is not None:
            query["price"]["$lte"] = max_price
            
    skip = (page - 1) * limit
    cursor = collection.find(query).skip(skip).limit(limit)
    
    if sort == "price_asc":
        cursor = cursor.sort("price", 1)
    elif sort == "price_desc":
        cursor = cursor.sort("price", -1)
        
    products = list(cursor)
    return [{**p, "id": str(p["_id"])} for p in products]

@router.get("/search", response_model=List[ProductResponse])
def search_products(q: str):
    collection = mongodb.get_collection("products")
    query = {
        "$or": [
            {"name": {"$regex": q, "$options": "i"}},
            {"description": {"$regex": q, "$options": "i"}},
            {"category": {"$regex": q, "$options": "i"}}
        ]
    }
    products = list(collection.find(query))
    return [{**p, "id": str(p["_id"])} for p in products]

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: str):
    collection = mongodb.get_collection("products")
    try:
        p = collection.find_one({"_id": ObjectId(product_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID")
        
    if not p:
        raise HTTPException(status_code=404, detail="Product not found")
    return {**p, "id": str(p["_id"])}

@router.put("/{product_id}", response_model=ProductResponse)
def update_product(product_id: str, product: ProductUpdate):
    collection = mongodb.get_collection("products")
    update_data = {k: v for k, v in product.model_dump().items() if v is not None}
    
    if not update_data:
        raise HTTPException(status_code=400, detail="No valid fields to update")
        
    try:
        result = collection.update_one(
            {"_id": ObjectId(product_id)},
            {"$set": update_data}
        )
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID")
        
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
        
    p = collection.find_one({"_id": ObjectId(product_id)})
    return {**p, "id": str(p["_id"])}

@router.patch("/{product_id}/stock", response_model=dict)
def update_stock(product_id: str, stock_update: ProductStockUpdate):
    collection = mongodb.get_collection("products")
    try:
        result = collection.update_one(
            {"_id": ObjectId(product_id)},
            {"$set": {"stock": stock_update.stock}}
        )
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID")
        
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
        
    return {"message": "Stock updated successfully"}

@router.delete("/{product_id}")
def delete_product(product_id: str):
    collection = mongodb.get_collection("products")
    try:
        result = collection.delete_one({"_id": ObjectId(product_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID")
        
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
        
    return {"message": "Product deleted"}
