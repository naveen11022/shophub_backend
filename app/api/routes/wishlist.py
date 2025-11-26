from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.wishlist import Wishlist
from app.models.product import Product
from app.schemas.wishlist import WishlistResponse

router = APIRouter()


@router.get("/wishlist", response_model=List[WishlistResponse])
def get_wishlist(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    wishlist = db.query(Wishlist).filter(Wishlist.user_id == current_user.id).all()
    return wishlist


@router.post("/wishlist/{product_id}", response_model=WishlistResponse)
def add_to_wishlist(
    product_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Check if product exists
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Check if already in wishlist
    existing = db.query(Wishlist).filter(
        Wishlist.user_id == current_user.id,
        Wishlist.product_id == product_id
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Product already in wishlist")
    
    wishlist_item = Wishlist(user_id=current_user.id, product_id=product_id)
    db.add(wishlist_item)
    db.commit()
    db.refresh(wishlist_item)
    return wishlist_item


@router.delete("/wishlist/{product_id}")
def remove_from_wishlist(
    product_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    wishlist_item = db.query(Wishlist).filter(
        Wishlist.user_id == current_user.id,
        Wishlist.product_id == product_id
    ).first()
    
    if not wishlist_item:
        raise HTTPException(status_code=404, detail="Item not in wishlist")
    
    db.delete(wishlist_item)
    db.commit()
    return {"message": "Removed from wishlist"}
