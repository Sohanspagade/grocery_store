from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.mongodb import mongodb
from app.routes import auth, users, categories, products, cart, orders, admin, ai

app = FastAPI(
    title="SmartCart AI",
    description="Grocery Management & AI Shopping API",
    version="1.0.0"
)

@app.get("/", tags=["Root"])
def read_root():
    return {
        "message": "Welcome to the SmartCart AI Backend API!",
        "docs": "Visit /docs for the API documentation."
    }

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:8080",
        "http://localhost:8081"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health Checks
@app.get("/api/health", tags=["Health"])
def health_check():
    return {
        "status": "ok",
        "service": "SmartCart Backend"
    }

@app.get("/api/health/db", tags=["Health"])
def health_db():
    try:
        # verify ping
        mongodb.client.admin.command('ping')
        return {
            "status": "ok",
            "database": "MongoDB Atlas connected"
        }
    except Exception as e:
        return {
            "status": "error",
            "database": str(e)
        }

# Include Routers
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(categories.router, prefix="/api/categories", tags=["Categories"])
app.include_router(products.router, prefix="/api/products", tags=["Products"])
app.include_router(cart.router, prefix="/api/cart", tags=["Cart"])
app.include_router(orders.router, prefix="/api/orders", tags=["Orders"])
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])
app.include_router(ai.router, prefix="/api/ai", tags=["AI"])

@app.on_event("startup")
async def startup_event():
    # Attempt to connect to DB during startup
    # Note: mongodb.connect() already prints on success
    mongodb.connect()
