from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.review import Review
from app.models.product import Product
from app.schemas.review import ReviewCreate, ReviewResponse

router = APIRouter()


@router.post("/reviews", response_model=ReviewResponse)
def create_review(
    review_data: ReviewCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Check if product exists
    product = db.query(Product).filter(Product.id == review_data.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Check if user already reviewed
    existing_review = db.query(Review).filter(
        Review.user_id == current_user.id,
        Review.product_id == review_data.product_id
    ).first()
    
    if existing_review:
        raise HTTPException(status_code=400, detail="You already reviewed this product")
    
    # Create review
    review = Review(
        user_id=current_user.id,
        **review_data.dict()
    )
    db.add(review)
    
    # Update product rating
    avg_rating = db.query(func.avg(Review.rating)).filter(
        Review.product_id == review_data.product_id
    ).scalar() or 0
    
    review_count = db.query(func.count(Review.id)).filter(
        Review.product_id == review_data.product_id
    ).scalar() or 0
    
    product.rating = round(avg_rating, 1)
    product.review_count = review_count + 1
    
    db.commit()
    db.refresh(review)
    return review


@router.get("/products/{product_id}/reviews", response_model=List[ReviewResponse])
def get_product_reviews(
    product_id: int,
    db: Session = Depends(get_db)
):
    reviews = db.query(Review).filter(
        Review.product_id == product_id
    ).order_by(Review.created_at.desc()).all()
    return reviews
