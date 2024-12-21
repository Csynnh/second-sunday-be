from pydantic import BaseModel
from typing import Optional, List


class SizeBase(BaseModel):
    name: str
    inventory: int

class SizeResponse(SizeBase):
    id: int
    sold: Optional[int] = 0

class SizeRequest(SizeBase):
    pass

class ColorBase(BaseModel):
    name: str
    images: Optional[List[str]]
    sizes: List[SizeBase]

class ColorResponse(ColorBase):
    id: int
    sizes: List[SizeResponse]


class ProductBase(BaseModel):
    name: str
    description: Optional[str]
    price: float
    material: Optional[str] = None
    policy: Optional[str] = None
    care_instructions: Optional[str] = None
    rating: Optional[float] = None
    category_id: int
    colors: List[ColorBase]


class ProductRequest(ProductBase):
    pass


class ProductResponse(ProductBase):
    id: int
    colors: List[ColorResponse]

    class Config:
        from_attributes = True

