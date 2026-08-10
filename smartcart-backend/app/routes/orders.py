from fastapi import APIRouter, HTTPException, status
from typing import List
from datetime import datetime
from bson import ObjectId
from app.schemas.order import OrderCreate, OrderStatusUpdate, OrderResponse
from app.database.mongodb import mongodb

router = APIRouter()

@router.post("/", response_model=OrderResponse)
def create_order(order: OrderCreate):
    cart_collection = mongodb.get_collection("cart_items")
    products_collection = mongodb.get_collection("products")
    orders_collection = mongodb.get_collection("orders")
    
    # Get user's cart
    cart_items = list(cart_collection.find({"user_id": order.user_id}))
    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")
        
    items = []
    subtotal = 0.0
    
    # Verify stock and calculate
    for item in cart_items:
        try:
            product = products_collection.find_one({"_id": ObjectId(item["product_id"])})
        except Exception:
            continue
            
        if not product:
            raise HTTPException(status_code=400, detail=f"Product {item['product_id']} not found")
            
        if product.get("stock", 0) < item["quantity"]:
            raise HTTPException(status_code=400, detail=f"Not enough stock for {product['name']}")
            
        item_subtotal = product["price"] * item["quantity"]
        subtotal += item_subtotal
        
        items.append({
            "product_id": item["product_id"],
            "name": product["name"],
            "price": product["price"],
            "quantity": item["quantity"],
            "subtotal": item_subtotal
        })
        
    delivery_fee = 0.0 if subtotal >= 500 else 40.0
    total = subtotal + delivery_fee
    
    order_dict = {
        "user_id": order.user_id,
        "items": items,
        "subtotal": subtotal,
        "delivery_fee": delivery_fee,
        "total": total,
        "delivery_address": order.delivery_address,
        "payment_method": order.payment_method,
        "status": "pending",
        "created_at": datetime.utcnow()
    }
    
    # Create order
    result = orders_collection.insert_one(order_dict)
    
    # Reduce product stock
    for item in items:
        products_collection.update_one(
            {"_id": ObjectId(item["product_id"])},
            {"$inc": {"stock": -item["quantity"]}}
        )
        
    # Clear cart
    cart_collection.delete_many({"user_id": order.user_id})
    
    order_dict["id"] = str(result.inserted_id)
    return order_dict

@router.get("/{user_id}", response_model=List[OrderResponse])
def get_user_orders(user_id: str):
    orders_collection = mongodb.get_collection("orders")
    orders = list(orders_collection.find({"user_id": user_id}).sort("created_at", -1))
    return [{**o, "id": str(o["_id"])} for o in orders]

@router.get("/detail/{order_id}", response_model=OrderResponse)
def get_order(order_id: str):
    orders_collection = mongodb.get_collection("orders")
    try:
        order = orders_collection.find_one({"_id": ObjectId(order_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid order ID")
        
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
        
    return {**order, "id": str(order["_id"])}

@router.patch("/{order_id}/status", response_model=OrderResponse)
def update_order_status(order_id: str, status_update: OrderStatusUpdate):
    valid_statuses = ["pending", "confirmed", "packed", "out_for_delivery", "delivered", "cancelled"]
    if status_update.status not in valid_statuses:
        raise HTTPException(status_code=400, detail="Invalid status")
        
    orders_collection = mongodb.get_collection("orders")
    try:
        result = orders_collection.update_one(
            {"_id": ObjectId(order_id)},
            {"$set": {"status": status_update.status}}
        )
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid order ID")
        
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Order not found")
        
    order = orders_collection.find_one({"_id": ObjectId(order_id)})
    return {**order, "id": str(order["_id"])}

@router.delete("/{order_id}")
def cancel_order(order_id: str):
    orders_collection = mongodb.get_collection("orders")
    try:
        order = orders_collection.find_one({"_id": ObjectId(order_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid order ID")
        
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
        
    if order["status"] not in ["pending", "confirmed"]:
        raise HTTPException(status_code=400, detail="Cannot cancel order in this status")
        
    orders_collection.update_one(
        {"_id": ObjectId(order_id)},
        {"$set": {"status": "cancelled"}}
    )
    
    # Restore stock
    products_collection = mongodb.get_collection("products")
    for item in order["items"]:
        products_collection.update_one(
            {"_id": ObjectId(item["product_id"])},
            {"$inc": {"stock": item["quantity"]}}
        )
        
    return {"message": "Order cancelled successfully"}
