from fastapi import APIRouter, HTTPException, status
from typing import List
from bson import ObjectId
from app.schemas.category import CategoryCreate, CategoryResponse
from app.database.mongodb import mongodb

router = APIRouter()

@router.post("/", response_model=CategoryResponse)
def create_category(category: CategoryCreate):
    collection = mongodb.get_collection("categories")
    cat_dict = category.model_dump()
    result = collection.insert_one(cat_dict)
    return {**cat_dict, "id": str(result.inserted_id)}

@router.get("/", response_model=List[CategoryResponse])
def get_categories():
    collection = mongodb.get_collection("categories")
    categories = list(collection.find())
    return [{**cat, "id": str(cat["_id"])} for cat in categories]

@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(category_id: str):
    collection = mongodb.get_collection("categories")
    try:
        cat = collection.find_one({"_id": ObjectId(category_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID")
    
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")
    return {**cat, "id": str(cat["_id"])}

@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(category_id: str, category: CategoryCreate):
    collection = mongodb.get_collection("categories")
    try:
        result = collection.update_one(
            {"_id": ObjectId(category_id)},
            {"$set": category.model_dump()}
        )
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID")
        
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Category not found")
        
    return {**category.model_dump(), "id": category_id}

@router.delete("/{category_id}")
def delete_category(category_id: str):
    collection = mongodb.get_collection("categories")
    try:
        result = collection.delete_one({"_id": ObjectId(category_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID")
        
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Category not found")
        
    return {"message": "Category deleted"}
