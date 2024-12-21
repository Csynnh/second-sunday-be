# app/main.py
from fastapi import FastAPI
from app.routes import categorys, products

app = FastAPI()

# Include the product endpoints (routes)
app.include_router(products.router, prefix="/products", tags=["products"])
app.include_router(categorys.router, prefix="/categories", tags=["categories"])


@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI app!"}
