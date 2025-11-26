"""Create all database tables"""
from app.core.database import engine, Base

# Import all models to register them with Base
from app.models.user import User
from app.models.product import Product, Category
from app.models.cart import Cart, CartItem
from app.models.order import Order, OrderItem
from app.models.review import Review
from app.models.wishlist import Wishlist
from app.models.banner import Banner

def create_tables():
    print("Creating all tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")

if __name__ == "__main__":
    create_tables()
