from pydantic import BaseModel
from datetime import datetime
from .product import ProductResponse


class WishlistResponse(BaseModel):
    id: int
    product_id: int
    created_at: datetime
    product: ProductResponse

    class Config:
        from_attributes = True
