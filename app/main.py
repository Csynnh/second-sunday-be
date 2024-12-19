# app/main.py
from fastapi import FastAPI
from routes.products import router as product_router

app = FastAPI()

# Include the product endpoints (routes)
app.include_router(product_router, prefix="/products", tags=["products"])


@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI app!"}
