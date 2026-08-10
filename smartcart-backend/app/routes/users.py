from fastapi import APIRouter, HTTPException, status
from typing import List
from bson import ObjectId
from app.schemas.user import UserResponse
from app.database.mongodb import mongodb
from app.utils.helpers import serialize_list

router = APIRouter()

@router.get("/", response_model=List[UserResponse])
def get_users():
    users_collection = mongodb.get_collection("users")
    users = list(users_collection.find())
    
    # Exclude passwords and convert _id to id
    out_users = []
    for user in users:
        user_dict = {
            "id": str(user["_id"]),
            "name": user["name"],
            "email": user["email"],
            "role": user.get("role", "customer")
        }
        out_users.append(user_dict)
    return out_users

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: str):
    users_collection = mongodb.get_collection("users")
    try:
        user = users_collection.find_one({"_id": ObjectId(user_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid user ID format")
        
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "role": user.get("role", "customer")
    }

@router.delete("/{user_id}")
def delete_user(user_id: str):
    users_collection = mongodb.get_collection("users")
    try:
        result = users_collection.delete_one({"_id": ObjectId(user_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid user ID format")
        
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
        
    return {"message": "User deleted successfully"}
