from pydantic import BaseModel
from typing import Optional, List, Dict


class InventoryItem(BaseModel):
    color: str
    size: str
    quantity: int


class ProductBase(BaseModel):
    name: str
    price: float
    description: Optional[str] = None
    images: Optional[List[str]] = None  # List of image URLs
    colors: List[str]  # Available colors
    sizes: List[str]  # Available sizes
    inventory: List[InventoryItem]  # Inventory details for each color and size


class ProductOut(ProductBase):
    id: int

    class Config:
        from_attributes = True


class ProductCreate(ProductBase):
    pass

class SizeBase(BaseModel):
    name: str
    inventory: int

class SizeResponse(SizeBase):
    id: int

class SizeRequest(SizeBase):
    pass

class ColorBase(BaseModel):
    name: str
    images: Optional[List[str]]
    sizes: List[SizeRequest]

class ColorResponse(ColorBase):
    id: int
    sizes: List[SizeResponse]

class ColorRequest(ColorBase):
    pass

class ProductRequest(BaseModel):
    name: str
    description: Optional[str]
    price: float
    colors: List[ColorRequest]


class ProductResponse(ProductRequest):
    id: int

    class Config:
        from_attributes = True

