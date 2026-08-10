from fastapi import APIRouter, HTTPException, status
from typing import List
from datetime import datetime
from bson import ObjectId
import json
import httpx
import re

from app.schemas.ai import (
    ChatRequest, ChatResponse, 
    ShoppingListRequest, ShoppingListResponse,
    RecommendationsRequest, SearchRequest
)
from app.schemas.product import ProductResponse
from app.database.mongodb import mongodb
from app.services.openrouter import call_openrouter

router = APIRouter()

SYSTEM_PROMPT = """You are SmartCart AI, a helpful grocery shopping assistant.
You help users:
- find grocery products
- create shopping lists
- recommend products
- plan grocery purchases
- suggest products within a budget

Only recommend products that exist in the provided database context.
Do not invent product names or prices.
If the requested product is unavailable, clearly tell the user.
Prices are in Indian Rupees (INR).
Be concise and practical."""

def extract_json(content: str) -> dict:
    try:
        # Try to parse the raw string directly
        return json.loads(content)
    except json.JSONDecodeError:
        # If it's wrapped in markdown code blocks, extract it
        match = re.search(r'```json\n(.*?)\n```', content, re.DOTALL)
        if match:
            return json.loads(match.group(1))
        # Another pattern just in case
        match = re.search(r'\{.*\}', content, re.DOTALL)
        if match:
            return json.loads(match.group(0))
        raise

@router.post("/chat", response_model=ChatResponse)
async def ai_chat(request: ChatRequest):
    products_coll = mongodb.get_collection("products")
    # Get a sample of products for context (in a real app this would be vector search or full-text search)
    # Since it's simple, let's just pass all active products names and categories if not too large, or a subset.
    products = list(products_coll.find({}, {"name": 1, "category": 1, "price": 1, "stock": 1}).limit(50))
    context = json.dumps([{**p, "_id": str(p["_id"])} for p in products])
    
    prompt = f"Context (Available Products in DB):\n{context}\n\nUser Message: {request.message}"
    
    try:
        reply = await call_openrouter(SYSTEM_PROMPT, prompt)
    except Exception as e:
        raise HTTPException(status_code=503, detail="AI service is temporarily unavailable")
        
    conv_coll = mongodb.get_collection("ai_conversations")
    conv = {
        "user_id": request.user_id,
        "message": request.message,
        "reply": reply,
        "created_at": datetime.utcnow()
    }
    result = conv_coll.insert_one(conv)
    
    return {
        "message": reply,
        "conversation_id": str(result.inserted_id)
    }

@router.post("/shopping-list", response_model=ShoppingListResponse)
async def ai_shopping_list(request: ShoppingListRequest):
    products_coll = mongodb.get_collection("products")
    products = list(products_coll.find({}, {"name": 1, "category": 1, "price": 1, "unit": 1}))
    context = json.dumps([{**p, "_id": str(p["_id"])} for p in products])
    
    system_prompt = SYSTEM_PROMPT + "\nYou must output ONLY valid JSON format containing a list of recommended products and the estimated total. Schema: { 'shopping_list': [{ 'product_id': 'id', 'name': 'name', 'quantity': 1, 'unit': 'kg', 'price': 10 }], 'estimated_total': 100 }"
    
    user_prompt = f"Context (Available Products):\n{context}\n\nRequest: Need a grocery list for {request.people} people for {request.days} days. Budget: {request.budget}. Diet: {request.diet}. Reqs: {request.requirements or 'None'}"
    
    try:
        reply = await call_openrouter(system_prompt, user_prompt)
        parsed_data = extract_json(reply)
    except Exception as e:
        raise HTTPException(status_code=503, detail="AI service is temporarily unavailable")
        
    # Verify products and calculate actual total
    actual_list = []
    actual_total = 0.0
    
    for item in parsed_data.get("shopping_list", []):
        try:
            db_product = products_coll.find_one({"_id": ObjectId(item["product_id"])})
            if db_product:
                qty = int(item.get("quantity", 1))
                price = db_product["price"]
                actual_list.append({
                    "product_id": str(db_product["_id"]),
                    "name": db_product["name"],
                    "quantity": qty,
                    "unit": db_product["unit"],
                    "price": price
                })
                actual_total += qty * price
        except Exception:
            continue
            
    return {
        "shopping_list": actual_list,
        "estimated_total": actual_total
    }

@router.post("/recommendations", response_model=List[ProductResponse])
async def ai_recommendations(request: RecommendationsRequest):
    orders_coll = mongodb.get_collection("orders")
    products_coll = mongodb.get_collection("products")
    
    orders = list(orders_coll.find({"user_id": request.user_id}).sort("created_at", -1).limit(3))
    purchased_items = []
    for order in orders:
        for item in order.get("items", []):
            purchased_items.append(item["name"])
            
    products = list(products_coll.find({}))
    context = json.dumps([{**p, "_id": str(p["_id"])} for p in products])
    
    system_prompt = SYSTEM_PROMPT + "\nYou must output ONLY valid JSON format containing a list of recommended product IDs based on the user's past purchases. Schema: { 'recommended_ids': ['id1', 'id2'] }"
    
    user_prompt = f"Context (Available Products):\n{context}\n\nUser recently bought: {', '.join(purchased_items)}. Recommend up to 5 complementary products."
    
    try:
        reply = await call_openrouter(system_prompt, user_prompt)
        parsed_data = extract_json(reply)
    except Exception as e:
        raise HTTPException(status_code=503, detail="AI service is temporarily unavailable")
        
    recommended_ids = parsed_data.get("recommended_ids", [])
    
    recommended_products = []
    for pid in recommended_ids:
        try:
            p = products_coll.find_one({"_id": ObjectId(pid)})
            if p:
                recommended_products.append({**p, "id": str(p["_id"])})
        except Exception:
            pass
            
    return recommended_products

@router.post("/search", response_model=List[ProductResponse])
async def ai_search(request: SearchRequest):
    system_prompt = """You convert natural language search queries for grocery products into structured JSON intent.
Schema: { "category": "Category Name or null", "max_price": float or null, "keywords": ["word1"] }
Output ONLY JSON."""

    try:
        reply = await call_openrouter(system_prompt, f"Query: {request.query}")
        intent = extract_json(reply)
    except Exception as e:
        raise HTTPException(status_code=503, detail="AI service is temporarily unavailable")
        
    query = {}
    
    if intent.get("category"):
        query["category"] = {"$regex": f"^{intent['category']}$", "$options": "i"}
        
    if intent.get("max_price") is not None:
        query["price"] = {"$lte": float(intent["max_price"])}
        
    if intent.get("keywords"):
        # Match any of the keywords in name or description
        keyword_regex = "|".join(intent["keywords"])
        query["$or"] = [
            {"name": {"$regex": keyword_regex, "$options": "i"}},
            {"description": {"$regex": keyword_regex, "$options": "i"}}
        ]
        
    products_coll = mongodb.get_collection("products")
    products = list(products_coll.find(query).limit(20))
    
    return [{**p, "id": str(p["_id"])} for p in products]
