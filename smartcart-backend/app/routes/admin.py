from fastapi import APIRouter, HTTPException
from typing import List
from app.database.mongodb import mongodb
from app.schemas.order import OrderResponse
from app.schemas.product import ProductResponse

router = APIRouter()

@router.get("/dashboard", response_model=dict)
def get_dashboard_stats():
    users_coll = mongodb.get_collection("users")
    products_coll = mongodb.get_collection("products")
    orders_coll = mongodb.get_collection("orders")
    
    total_users = users_coll.count_documents({})
    total_products = products_coll.count_documents({})
    total_orders = orders_coll.count_documents({})
    
    # Revenue (only from delivered/completed orders usually, but we'll sum all non-cancelled)
    pipeline = [
        {"$match": {"status": {"$ne": "cancelled"}}},
        {"$group": {"_id": None, "total_revenue": {"$sum": "$total"}}}
    ]
    revenue_result = list(orders_coll.aggregate(pipeline))
    total_revenue = revenue_result[0]["total_revenue"] if revenue_result else 0
    
    low_stock = products_coll.count_documents({"stock": {"$lte": 5}})
    
    return {
        "total_users": total_users,
        "total_products": total_products,
        "total_orders": total_orders,
        "total_revenue": total_revenue,
        "low_stock_products": low_stock
    }

@router.get("/orders", response_model=List[OrderResponse])
def get_all_orders():
    orders_collection = mongodb.get_collection("orders")
    orders = list(orders_collection.find().sort("created_at", -1))
    return [{**o, "id": str(o["_id"])} for o in orders]

@router.get("/low-stock", response_model=List[ProductResponse])
def get_low_stock_products():
    products_coll = mongodb.get_collection("products")
    products = list(products_coll.find({"stock": {"$lte": 5}}))
    return [{**p, "id": str(p["_id"])} for p in products]
