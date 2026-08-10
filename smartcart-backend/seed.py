from pymongo import MongoClient
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

MONGO_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("MONGODB_DATABASE", "smartcart")

def seed():
    print("Connecting to MongoDB Atlas...")
    try:
        client = MongoClient(MONGO_URI)
        client.admin.command('ping')
    except Exception as e:
        print(f"Failed to connect: {e}")
        return

    db = client[DB_NAME]
    print(f"Connected to db: {DB_NAME}")

    users_coll = db["users"]
    categories_coll = db["categories"]
    products_coll = db["products"]

    # Seed Users
    admin_email = "admin@smartcart.com"
    if not users_coll.find_one({"email": admin_email}):
        users_coll.insert_one({
            "name": "Admin",
            "email": admin_email,
            "password": "Admin@123",
            "role": "admin",
            "created_at": datetime.utcnow()
        })
        print("Admin user seeded.")
        
    customer_email = "customer@smartcart.com"
    if not users_coll.find_one({"email": customer_email}):
        users_coll.insert_one({
            "name": "Customer",
            "email": customer_email,
            "password": "Customer@123",
            "role": "customer",
            "created_at": datetime.utcnow()
        })
        print("Customer user seeded.")

    # Seed Categories
    cats_to_seed = [
        {"name": "Dairy", "description": "Milk, Cheese, and Dairy products"},
        {"name": "Vegetables", "description": "Fresh vegetables"},
        {"name": "Fruits", "description": "Fresh fruits"},
        {"name": "Snacks", "description": "Chips, Biscuits, and quick bites"},
        {"name": "Beverages", "description": "Juices, Soft drinks, Tea, Coffee"},
        {"name": "Meat", "description": "Fresh meat and poultry"},
        {"name": "Bakery", "description": "Breads and baked goods"},
        {"name": "Spices", "description": "Indian spices and condiments"},
        {"name": "Grains", "description": "Rice, Wheat, Pulses"},
        {"name": "Personal Care", "description": "Soaps, Shampoos, Lotions"}
    ]
    
    for c in cats_to_seed:
        if not categories_coll.find_one({"name": c["name"]}):
            categories_coll.insert_one(c)
    print("Categories seeded.")

    # Seed Products (Sample)
    products_to_seed = [
        {"name": "Amul Taza Milk", "description": "Toned Milk", "category": "Dairy", "price": 54, "original_price": 54, "unit": "1L", "stock": 100, "rating": 4.5},
        {"name": "Amul Butter", "description": "Pasteurised Butter", "category": "Dairy", "price": 56, "original_price": 58, "unit": "100g", "stock": 50, "rating": 4.8},
        {"name": "Onion", "description": "Fresh red onions", "category": "Vegetables", "price": 40, "original_price": 50, "unit": "1kg", "stock": 200, "rating": 4.2},
        {"name": "Tomato", "description": "Local tomatoes", "category": "Vegetables", "price": 30, "original_price": 40, "unit": "1kg", "stock": 150, "rating": 4.1},
        {"name": "Potato", "description": "Fresh potatoes", "category": "Vegetables", "price": 25, "original_price": 35, "unit": "1kg", "stock": 300, "rating": 4.0},
        {"name": "Apple - Fuji", "description": "Sweet fuji apples", "category": "Fruits", "price": 150, "original_price": 180, "unit": "1kg", "stock": 50, "rating": 4.6},
        {"name": "Banana - Robusta", "description": "Fresh bananas", "category": "Fruits", "price": 60, "original_price": 70, "unit": "1kg", "stock": 100, "rating": 4.5},
        {"name": "Lays India's Magic Masala", "description": "Potato chips", "category": "Snacks", "price": 20, "original_price": 20, "unit": "50g", "stock": 120, "rating": 4.7},
        {"name": "Britannia Good Day", "description": "Butter Cookies", "category": "Snacks", "price": 30, "original_price": 30, "unit": "75g", "stock": 100, "rating": 4.6},
        {"name": "Coca Cola", "description": "Soft drink", "category": "Beverages", "price": 40, "original_price": 40, "unit": "750ml", "stock": 80, "rating": 4.3},
        {"name": "Brooke Bond Red Label", "description": "Tea powder", "category": "Beverages", "price": 120, "original_price": 130, "unit": "250g", "stock": 60, "rating": 4.5},
        {"name": "Nescafe Classic", "description": "Instant coffee", "category": "Beverages", "price": 150, "original_price": 160, "unit": "50g", "stock": 40, "rating": 4.8},
        {"name": "Chicken Breast", "description": "Boneless chicken breast", "category": "Meat", "price": 250, "original_price": 280, "unit": "500g", "stock": 20, "rating": 4.5},
        {"name": "Eggs - Regular", "description": "Farm eggs", "category": "Meat", "price": 60, "original_price": 70, "unit": "6 pcs", "stock": 60, "rating": 4.2},
        {"name": "Modern Bread", "description": "White bread", "category": "Bakery", "price": 40, "original_price": 45, "unit": "400g", "stock": 30, "rating": 4.1},
        {"name": "MDH Garam Masala", "description": "Mixed spices", "category": "Spices", "price": 75, "original_price": 80, "unit": "100g", "stock": 100, "rating": 4.7},
        {"name": "Everest Turmeric Powder", "description": "Haldi", "category": "Spices", "price": 30, "original_price": 35, "unit": "100g", "stock": 90, "rating": 4.6},
        {"name": "India Gate Basmati Rice", "description": "Premium basmati", "category": "Grains", "price": 450, "original_price": 500, "unit": "5kg", "stock": 40, "rating": 4.8},
        {"name": "Aashirvaad Atta", "description": "Whole wheat atta", "category": "Grains", "price": 220, "original_price": 240, "unit": "5kg", "stock": 70, "rating": 4.7},
        {"name": "Toor Dal", "description": "Yellow pigeon peas", "category": "Grains", "price": 160, "original_price": 180, "unit": "1kg", "stock": 80, "rating": 4.4},
        {"name": "Dove Soap", "description": "Beauty bathing bar", "category": "Personal Care", "price": 50, "original_price": 55, "unit": "100g", "stock": 100, "rating": 4.5},
        {"name": "Head & Shoulders", "description": "Anti-dandruff shampoo", "category": "Personal Care", "price": 150, "original_price": 170, "unit": "180ml", "stock": 60, "rating": 4.3},
        {"name": "Amul Curd", "description": "Fresh curd", "category": "Dairy", "price": 40, "original_price": 45, "unit": "500g", "stock": 50, "rating": 4.6},
        {"name": "Paneer", "description": "Fresh malai paneer", "category": "Dairy", "price": 85, "original_price": 90, "unit": "200g", "stock": 40, "rating": 4.7},
        {"name": "Carrot", "description": "Ooty carrots", "category": "Vegetables", "price": 50, "original_price": 60, "unit": "1kg", "stock": 80, "rating": 4.3},
        {"name": "Grapes - Green", "description": "Seedless grapes", "category": "Fruits", "price": 90, "original_price": 110, "unit": "500g", "stock": 60, "rating": 4.4},
        {"name": "Kurkure Masala Munch", "description": "Corn puffs", "category": "Snacks", "price": 20, "original_price": 20, "unit": "90g", "stock": 100, "rating": 4.5},
        {"name": "Sprite", "description": "Lemon-lime soda", "category": "Beverages", "price": 40, "original_price": 40, "unit": "750ml", "stock": 80, "rating": 4.2},
        {"name": "Tata Salt", "description": "Iodized salt", "category": "Spices", "price": 25, "original_price": 28, "unit": "1kg", "stock": 200, "rating": 4.8},
        {"name": "MTR Puliogare Powder", "description": "Tamarind rice mix", "category": "Spices", "price": 45, "original_price": 50, "unit": "100g", "stock": 50, "rating": 4.6}
    ]
    
    for p in products_to_seed:
        if not products_coll.find_one({"name": p["name"]}):
            products_coll.insert_one(p)
    
    print("Products seeded. Total products in DB:", products_coll.count_documents({}))
    print("Database seeding completed.")

if __name__ == "__main__":
    seed()
