# SmartCart AI - Grocery Management & AI Shopping API

SmartCart AI is a fully functional REST API backend for a grocery management platform. It includes essential e-commerce capabilities such as product management, cart handling, and order processing, coupled with AI-powered features for intelligent shopping recommendations and list generation.

## Features

- **Authentication**: Simple registration and login (password hashed bypassed for development requirements).
- **Products & Categories**: Full CRUD, pagination, and stock management.
- **Cart & Orders**: Cart updates, total calculations, dynamic delivery fees, and order processing.
- **AI Integrations (OpenRouter)**:
  - Smart chat assistant for grocery queries.
  - Automated shopping list generation based on criteria (budget, diet, days).
  - Contextual product recommendations.
  - Natural language search.
- **Admin Dashboard**: Aggregated stats for products, orders, and revenue.

## Architecture

The backend is built with:
- **Python 3.11+**
- **FastAPI** & **Uvicorn**
- **MongoDB Atlas** (using raw **PyMongo**)
- **Pydantic** for validation
- **OpenRouter API** via **HTTPX**

## Requirements

Ensure you have Python 3.11+ installed. Install dependencies via:
```bash
pip install -r requirements.txt
```

## Setup

### 1. MongoDB Atlas Setup

1. Create a MongoDB Atlas cluster.
2. Create a database user with read/write access.
3. Whitelist your IP address (or allow from anywhere `0.0.0.0/0` for development).
4. Copy the connection string.
5. In the `.env` file, set `MONGODB_URI` to your connection string.
6. Example: `MONGODB_URI=mongodb+srv://USERNAME:PASSWORD@cluster0.mongodb.net/`

### 2. Environment Variables (.env)

Create a `.env` file in the root of the project (refer to `.env.example`). It should contain:
```
MONGODB_URI=mongodb+srv://USERNAME:PASSWORD@cluster.mongodb.net/
MONGODB_DATABASE=smartcart
OPENROUTER_API_KEY=your_openrouter_api_key
OPENROUTER_MODEL=openai/gpt-3.5-turbo
PORT=8000
```
> **Note:** The OpenRouter API key is already configured in the provided development environment.

## Running Locally

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the seed script to populate data:
   ```bash
   python seed.py
   ```
3. Start the FastAPI server:
   ```bash
   uvicorn app.main:app --reload
   ```

## API Documentation & Testing

FastAPI automatically generates interactive Swagger documentation.
- **Swagger URL**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc URL**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Testing Flow
1. Check **Health**: `GET /api/health` and `GET /api/health/db`.
2. Check **Auth**: Use `/api/auth/register` to register, or use the seeded users:
   - Admin: `admin@smartcart.com` / `Admin@123`
   - Customer: `customer@smartcart.com` / `Customer@123`
3. Check **Products**: Search using `GET /api/products?search=milk`
4. Add to **Cart**: `POST /api/cart`
5. Place **Order**: `POST /api/orders`
6. Test **AI Features**:
   - Try `POST /api/ai/chat` with a query like "Suggest something sweet".
   - Try `POST /api/ai/shopping-list` with a realistic budget.

## Troubleshooting

- **MongoDB Errors**: Ensure your IP is whitelisted in MongoDB Atlas and the URI is correct.
- **OpenRouter Errors**: Check if the `OPENROUTER_API_KEY` is set in the `.env` file and that you have available credits.

---
*Built for SmartCart AI Development Project*
