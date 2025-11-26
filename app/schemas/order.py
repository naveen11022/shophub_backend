from pydantic import BaseModel
from typing import List, Dict, Any
from datetime import datetime


class OrderItemBase(BaseModel):
    product_id: int
    quantity: int
    price: float


class OrderItemResponse(OrderItemBase):
    id: int

    class Config:
        from_attributes = True


class OrderCreate(BaseModel):
    shipping_address: Dict[str, Any]
    payment_method: str


class OrderResponse(BaseModel):
    id: int
    order_number: str
    status: str
    total_amount: float
    shipping_address: Dict[str, Any]
    payment_method: str
    payment_status: str
    created_at: datetime
    items: List[OrderItemResponse]

    class Config:
        from_attributes = True
