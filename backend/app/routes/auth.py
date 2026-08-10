from fastapi import APIRouter, HTTPException, status
from datetime import datetime
from bson import ObjectId
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.database.mongodb import mongodb

router = APIRouter()

@router.post("/register", response_model=dict)
def register(user: UserCreate):
    users_collection = mongodb.get_collection("users")
    
    # Check if email exists
    if users_collection.find_one({"email": user.email}):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Store user (plaintext password as requested)
    user_dict = user.model_dump()
    user_dict["created_at"] = datetime.utcnow()
    
    result = users_collection.insert_one(user_dict)
    
    user_out = {
        "id": str(result.inserted_id),
        "name": user.name,
        "email": user.email,
        "role": user.role
    }
    
    return {
        "message": "User registered successfully",
        "user": user_out
    }

@router.post("/login", response_model=dict)
def login(user: UserLogin):
    users_collection = mongodb.get_collection("users")
    
    db_user = users_collection.find_one({"email": user.email})
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid credentials"
        )
    
    # Direct password comparison
    if db_user.get("password") != user.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid credentials"
        )
        
    user_out = {
        "id": str(db_user["_id"]),
        "name": db_user["name"],
        "email": db_user["email"],
        "role": db_user.get("role", "customer")
    }
    
    return {
        "message": "Login successful",
        "user": user_out
    }
