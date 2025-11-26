from app.core.database import SessionLocal
from app.core.security import get_password_hash
from app.models.user import User
from app.models.product import Product, Category
from app.models.banner import Banner
from app.models.cart import Cart

def seed_database():
    db = SessionLocal()
    
    try:
        # Create admin user
        admin = User(
            email="admin@shophub.com",
            username="admin",
            full_name="Admin User",
            hashed_password=get_password_hash("admin123"),
            role="admin"
        )
        db.add(admin)
        
        # Create regular user
        user = User(
            email="user@shophub.com",
            username="johndoe",
            full_name="John Doe",
            phone="+1234567890",
            hashed_password=get_password_hash("user123"),
            role="user"
        )
        db.add(user)
        db.flush()
        
        # Create cart for user
        cart = Cart(user_id=user.id)
        db.add(cart)
        
        # Create categories
        categories_data = [
            {"name": "Electronics", "slug": "electronics", "description": "Electronic devices and gadgets"},
            {"name": "Fashion", "slug": "fashion", "description": "Clothing and accessories"},
            {"name": "Home & Kitchen", "slug": "home-kitchen", "description": "Home appliances and kitchenware"},
            {"name": "Books", "slug": "books", "description": "Books and literature"},
            {"name": "Sports", "slug": "sports", "description": "Sports equipment and gear"},
        ]
        
        categories = []
        for cat_data in categories_data:
            category = Category(**cat_data)
            db.add(category)
            categories.append(category)
        
        db.flush()
        
        # Create products
        products_data = [
            {
                "name": "Wireless Bluetooth Headphones",
                "slug": "wireless-bluetooth-headphones",
                "description": "Premium noise-cancelling wireless headphones with 30-hour battery life",
                "price": 199.99,
                "discount_price": 149.99,
                "brand": "AudioTech",
                "sku": "AT-WH-001",
                "stock": 50,
                "category_id": categories[0].id,
                "is_featured": True,
                "images": ["https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500"]
            },
            {
                "name": "Smart Watch Pro",
                "slug": "smart-watch-pro",
                "description": "Advanced fitness tracking with heart rate monitor and GPS",
                "price": 299.99,
                "discount_price": 249.99,
                "brand": "TechWear",
                "sku": "TW-SW-002",
                "stock": 30,
                "category_id": categories[0].id,
                "is_featured": True,
                "images": ["https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500"]
            },
            {
                "name": "Men's Casual T-Shirt",
                "slug": "mens-casual-tshirt",
                "description": "100% cotton comfortable t-shirt in multiple colors",
                "price": 29.99,
                "brand": "StyleHub",
                "sku": "SH-TS-003",
                "stock": 100,
                "category_id": categories[1].id,
                "images": ["https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=500"]
            },
            {
                "name": "Coffee Maker Deluxe",
                "slug": "coffee-maker-deluxe",
                "description": "Programmable coffee maker with thermal carafe",
                "price": 89.99,
                "discount_price": 69.99,
                "brand": "BrewMaster",
                "sku": "BM-CM-004",
                "stock": 25,
                "category_id": categories[2].id,
                "images": ["https://images.unsplash.com/photo-1517668808822-9ebb02f2a0e6?w=500"]
            },
            {
                "name": "The Great Novel",
                "slug": "the-great-novel",
                "description": "Bestselling fiction novel of the year",
                "price": 19.99,
                "brand": "BookPress",
                "sku": "BP-BK-005",
                "stock": 75,
                "category_id": categories[3].id,
                "images": ["https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=500"]
            },
            {
                "name": "Yoga Mat Premium",
                "slug": "yoga-mat-premium",
                "description": "Non-slip eco-friendly yoga mat with carrying strap",
                "price": 39.99,
                "brand": "FitLife",
                "sku": "FL-YM-006",
                "stock": 60,
                "category_id": categories[4].id,
                "is_featured": True,
                "images": ["https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?w=500"]
            },
        ]
        
        for prod_data in products_data:
            product = Product(**prod_data)
            db.add(product)
        
        # Create banners
        banners_data = [
            {
                "title": "Summer Sale",
                "subtitle": "Up to 50% off on selected items",
                "image": "https://images.unsplash.com/photo-1607082348824-0a96f2a4b9da?w=1200",
                "link": "/products?is_featured=true",
                "position": 1
            },
            {
                "title": "New Arrivals",
                "subtitle": "Check out our latest collection",
                "image": "https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=1200",
                "link": "/products",
                "position": 2
            },
        ]
        
        for banner_data in banners_data:
            banner = Banner(**banner_data)
            db.add(banner)
        
        db.commit()
        print("Database seeded successfully!")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
