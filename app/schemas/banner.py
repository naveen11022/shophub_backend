from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class BannerCreate(BaseModel):
    title: str
    subtitle: Optional[str] = None
    image: str
    link: Optional[str] = None
    position: int = 0


class BannerResponse(BannerCreate):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
