from fastapi import APIRouter, HTTPException, status
from bson import ObjectId
from app.schemas.cart import CartItemCreate, CartItemUpdate, CartResponse
from app.database.mongodb import mongodb

router = APIRouter()

@router.post("/", response_model=dict)
def add_to_cart(item: CartItemCreate):
    cart_collection = mongodb.get_collection("cart_items")
    products_collection = mongodb.get_collection("products")
    
    # Verify product exists and has stock
    try:
        product = products_collection.find_one({"_id": ObjectId(item.product_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid product ID")
        
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
        
    if product.get("stock", 0) < item.quantity:
        raise HTTPException(status_code=400, detail="Not enough stock")
        
    # Check if item already in cart
    existing_item = cart_collection.find_one({
        "user_id": item.user_id,
        "product_id": item.product_id
    })
    
    if existing_item:
        new_quantity = existing_item["quantity"] + item.quantity
        if product.get("stock", 0) < new_quantity:
            raise HTTPException(status_code=400, detail="Not enough stock for combined quantity")
            
        cart_collection.update_one(
            {"_id": existing_item["_id"]},
            {"$set": {"quantity": new_quantity}}
        )
    else:
        cart_collection.insert_one(item.model_dump())
        
    return {"message": "Item added to cart"}

@router.get("/{user_id}", response_model=CartResponse)
def get_cart(user_id: str):
    cart_collection = mongodb.get_collection("cart_items")
    products_collection = mongodb.get_collection("products")
    
    cart_items = list(cart_collection.find({"user_id": user_id}))
    
    items = []
    subtotal = 0.0
    
    for item in cart_items:
        try:
            product = products_collection.find_one({"_id": ObjectId(item["product_id"])})
            if product:
                item_subtotal = product["price"] * item["quantity"]
                subtotal += item_subtotal
                items.append({
                    "product_id": item["product_id"],
                    "name": product["name"],
                    "price": product["price"],
                    "quantity": item["quantity"],
                    "subtotal": item_subtotal
                })
        except Exception:
            continue
            
    delivery_fee = 0.0 if subtotal >= 500 else (40.0 if subtotal > 0 else 0.0)
    discount = 0.0
    total = subtotal + delivery_fee - discount
    
    return {
        "items": items,
        "subtotal": subtotal,
        "delivery_fee": delivery_fee,
        "discount": discount,
        "total": total
    }

@router.put("/{user_id}/{product_id}")
def update_cart_item(user_id: str, product_id: str, update: CartItemUpdate):
    cart_collection = mongodb.get_collection("cart_items")
    products_collection = mongodb.get_collection("products")
    
    try:
        product = products_collection.find_one({"_id": ObjectId(product_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid product ID")
        
    if product and product.get("stock", 0) < update.quantity:
        raise HTTPException(status_code=400, detail="Not enough stock")
        
    result = cart_collection.update_one(
        {"user_id": user_id, "product_id": product_id},
        {"$set": {"quantity": update.quantity}}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Item not found in cart")
        
    return {"message": "Cart item updated"}

@router.delete("/{user_id}/{product_id}")
def remove_cart_item(user_id: str, product_id: str):
    cart_collection = mongodb.get_collection("cart_items")
    result = cart_collection.delete_one({"user_id": user_id, "product_id": product_id})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Item not found in cart")
        
    return {"message": "Item removed from cart"}

@router.delete("/{user_id}")
def clear_cart(user_id: str):
    cart_collection = mongodb.get_collection("cart_items")
    cart_collection.delete_many({"user_id": user_id})
    return {"message": "Cart cleared"}
