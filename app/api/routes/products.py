from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from app.core.database import get_db
from app.api.deps import get_current_admin
from app.models.product import Product, Category
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse, CategoryCreate, CategoryResponse

router = APIRouter()


@router.get("/products")
def get_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(1000, ge=1, le=1000),
    category_id: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    min_price: Optional[str] = Query(None),
    max_price: Optional[str] = Query(None),
    brand: Optional[str] = Query(None),
    is_featured: Optional[bool] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Product).filter(Product.is_active == True)
    
    # Handle category_id (convert from string and check if not empty)
    if category_id and category_id.strip():
        try:
            cat_id = int(category_id)
            query = query.filter(Product.category_id == cat_id)
        except ValueError:
            pass
    
    # Handle search
    if search and search.strip():
        query = query.filter(
            or_(
                Product.name.ilike(f"%{search}%"),
                Product.description.ilike(f"%{search}%"),
                Product.brand.ilike(f"%{search}%")
            )
        )
    
    if min_price and min_price.strip():
        try:
            min_p = float(min_price)
            query = query.filter(Product.price >= min_p)
        except ValueError:
            pass
    
    if max_price and max_price.strip():
        try:
            max_p = float(max_price)
            query = query.filter(Product.price <= max_p)
        except ValueError:
            pass
    
    if brand and brand.strip():
        query = query.filter(Product.brand == brand)
    
    if is_featured is not None:
        query = query.filter(Product.is_featured == is_featured)
    
    total = query.count()
    products = query.offset(skip).limit(limit).all()
    
    # Convert to dict manually to avoid serialization issues
    products_list = []
    for product in products:
        products_list.append({
            "id": product.id,
            "name": product.name,
            "slug": product.slug,
            "description": product.description,
            "price": product.price,
            "discount_price": product.discount_price,
            "brand": product.brand,
            "sku": product.sku,
            "stock": product.stock,
            "images": product.images or [],
            "category_id": product.category_id,
            "is_featured": product.is_featured,
            "is_active": product.is_active,
            "rating": product.rating,
            "review_count": product.review_count,
            "created_at": product.created_at.isoformat() if product.created_at else None,
        })
    
    return {
        "products": products_list
    }


@router.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.post("/products", response_model=ProductResponse)
def create_product(
    product_data: ProductCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin)
):
    product = Product(**product_data.dict())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@router.put("/products/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin)
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    for key, value in product_data.dict(exclude_unset=True).items():
        setattr(product, key, value)
    
    db.commit()
    db.refresh(product)
    return product


@router.delete("/products/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin)
):
    from app.models.wishlist import Wishlist
    from app.models.cart import CartItem
    from app.models.review import Review
    from app.models.order import OrderItem
    
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Check if product is in any orders (don't delete if so)
    order_items = db.query(OrderItem).filter(OrderItem.product_id == product_id).count()
    if order_items > 0:
        raise HTTPException(
            status_code=400, 
            detail=f"Cannot delete product. It exists in {order_items} order(s). Consider deactivating instead."
        )
    
    # Delete related records
    db.query(Wishlist).filter(Wishlist.product_id == product_id).delete()
    db.query(CartItem).filter(CartItem.product_id == product_id).delete()
    db.query(Review).filter(Review.product_id == product_id).delete()
    
    db.delete(product)
    db.commit()
    return {"message": "Product deleted successfully"}


# Categories
@router.get("/categories", response_model=List[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    return db.query(Category).filter(Category.is_active == True).all()


@router.post("/categories", response_model=CategoryResponse)
def create_category(
    category_data: CategoryCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin)
):
    category = Category(**category_data.dict())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category
