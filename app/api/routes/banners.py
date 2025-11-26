from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.api.deps import get_current_admin
from app.models.banner import Banner
from app.schemas.banner import BannerCreate, BannerResponse

router = APIRouter()


@router.get("/banners", response_model=List[BannerResponse])
def get_banners(db: Session = Depends(get_db)):
    return db.query(Banner).filter(Banner.is_active == True).order_by(Banner.position).all()


@router.post("/banners", response_model=BannerResponse)
def create_banner(
    banner_data: BannerCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin)
):
    banner = Banner(**banner_data.dict())
    db.add(banner)
    db.commit()
    db.refresh(banner)
    return banner
