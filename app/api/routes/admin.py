from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.database import get_db
from app.api.deps import get_current_admin
from app.models.user import User
from app.models.product import Product
from app.models.order import Order

router = APIRouter()


@router.get("/admin/stats")
def get_admin_stats(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin)
):
    # Get total products
    total_products = db.query(func.count(Product.id)).scalar()
    
    # Get total orders
    total_orders = db.query(func.count(Order.id)).scalar()
    
    # Get total users
    total_users = db.query(func.count(User.id)).scalar()
    
    # Get total revenue
    total_revenue = db.query(func.sum(Order.total_amount)).scalar() or 0
    
    # Get recent orders
    recent_orders = db.query(Order).order_by(Order.created_at.desc()).limit(5).all()
    
    # Get low stock products
    low_stock = db.query(Product).filter(Product.stock < 10).limit(5).all()
    
    return {
        "total_products": total_products,
        "total_orders": total_orders,
        "total_users": total_users,
        "total_revenue": round(total_revenue, 2),
        "recent_orders": [
            {
                "id": order.id,
                "order_number": order.order_number,
                "total_amount": order.total_amount,
                "status": order.status,
                "created_at": order.created_at.isoformat()
            }
            for order in recent_orders
        ],
        "low_stock_products": [
            {
                "id": product.id,
                "name": product.name,
                "stock": product.stock,
                "price": product.price
            }
            for product in low_stock
        ]
    }


@router.get("/admin/users")
def get_all_users(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin)
):
    users = db.query(User).all()
    return [
        {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "full_name": user.full_name,
            "role": user.role,
            "is_active": user.is_active,
            "created_at": user.created_at.isoformat() if user.created_at else None
        }
        for user in users
    ]


@router.post("/admin/users")
def create_user(
    user_data: dict,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin)
):
    from app.core.security import get_password_hash
    
    # Check if user exists
    existing_user = db.query(User).filter(
        (User.email == user_data["email"]) | (User.username == user_data["username"])
    ).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    # Create new user
    hashed_password = get_password_hash(user_data["password"])
    new_user = User(
        email=user_data["email"],
        username=user_data["username"],
        full_name=user_data["full_name"],
        hashed_password=hashed_password,
        role=user_data.get("role", "customer"),
        is_active=user_data.get("is_active", True)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {
        "id": new_user.id,
        "email": new_user.email,
        "username": new_user.username,
        "full_name": new_user.full_name,
        "role": new_user.role,
        "is_active": new_user.is_active,
        "created_at": new_user.created_at.isoformat() if new_user.created_at else None
    }


@router.put("/admin/users/{user_id}")
def update_user(
    user_id: int,
    user_data: dict,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin)
):
    from app.core.security import get_password_hash
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update fields
    if "email" in user_data:
        user.email = user_data["email"]
    if "username" in user_data:
        user.username = user_data["username"]
    if "full_name" in user_data:
        user.full_name = user_data["full_name"]
    if "role" in user_data:
        user.role = user_data["role"]
    if "is_active" in user_data:
        user.is_active = user_data["is_active"]
    if "password" in user_data and user_data["password"]:
        user.hashed_password = get_password_hash(user_data["password"])
    
    db.commit()
    db.refresh(user)
    
    return {
        "id": user.id,
        "email": user.email,
        "username": user.username,
        "full_name": user.full_name,
        "role": user.role,
        "is_active": user.is_active,
        "created_at": user.created_at.isoformat() if user.created_at else None
    }


@router.delete("/admin/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Prevent deleting yourself
    if user.id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot delete your own account")
    
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}


# Category Management
@router.get("/admin/categories")
def get_all_categories(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin)
):
    from app.models.product import Category
    categories = db.query(Category).all()
    return [
        {
            "id": cat.id,
            "name": cat.name,
            "slug": cat.slug,
            "description": cat.description,
            "is_active": cat.is_active
        }
        for cat in categories
    ]


@router.put("/admin/categories/{category_id}")
def update_category(
    category_id: int,
    category_data: dict,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin)
):
    from app.models.product import Category
    
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    if "name" in category_data:
        category.name = category_data["name"]
    if "slug" in category_data:
        category.slug = category_data["slug"]
    if "description" in category_data:
        category.description = category_data["description"]
    if "is_active" in category_data:
        category.is_active = category_data["is_active"]
    
    db.commit()
    db.refresh(category)
    
    return {
        "id": category.id,
        "name": category.name,
        "slug": category.slug,
        "description": category.description,
        "is_active": category.is_active
    }


@router.delete("/admin/categories/{category_id}")
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin)
):
    from app.models.product import Category
    
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Check if category has products
    products_count = db.query(Product).filter(Product.category_id == category_id).count()
    if products_count > 0:
        raise HTTPException(
            status_code=400, 
            detail=f"Cannot delete category with {products_count} products. Please reassign or delete products first."
        )
    
    db.delete(category)
    db.commit()
    return {"message": "Category deleted successfully"}
