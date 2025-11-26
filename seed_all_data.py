"""Seed all data to PostgreSQL database"""
from app.core.database import SessionLocal, engine, Base
from app.core.security import get_password_hash
from app.models.user import User
from app.models.product import Product, Category
from app.models.banner import Banner
from app.models.cart import Cart
import random

def seed_database():
    # Create tables first
    from app.models.order import Order, OrderItem
    from app.models.review import Review
    from app.models.wishlist import Wishlist
    
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created!")
    
    db = SessionLocal()
    
    try:
        # Check if data already exists
        existing_users = db.query(User).count()
        if existing_users > 0:
            print(f"Database already has {existing_users} users. Skipping seed.")
            return
        
        print("Seeding users...")
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
            role="customer"
        )
        db.add(user)
        db.flush()
        
        # Create cart for user
        cart = Cart(user_id=user.id)
        db.add(cart)
        
        print("Seeding categories...")
        categories_data = [
            {"name": "Electronics", "slug": "electronics", "description": "Electronic devices and gadgets"},
            {"name": "Fashion", "slug": "fashion", "description": "Clothing and accessories"},
            {"name": "Home & Kitchen", "slug": "home-kitchen", "description": "Home appliances and kitchenware"},
            {"name": "Books", "slug": "books", "description": "Books and literature"},
            {"name": "Sports", "slug": "sports", "description": "Sports equipment and gear"},
            {"name": "Beauty", "slug": "beauty", "description": "Beauty and personal care"},
            {"name": "Toys", "slug": "toys", "description": "Toys and games"},
            {"name": "Automotive", "slug": "automotive", "description": "Automotive parts and accessories"},
        ]
        
        categories = []
        for cat_data in categories_data:
            category = Category(**cat_data)
            db.add(category)
            categories.append(category)
        db.flush()
        
        print("Seeding products...")
        # Product data with variety
        products_data = []
        
        # Electronics
        electronics = [
            ("Wireless Bluetooth Headphones", "Premium noise-cancelling wireless headphones", 199.99, 149.99, "AudioTech", 50),
            ("Smart Watch Pro", "Advanced fitness tracking smartwatch", 299.99, 249.99, "TechWear", 30),
            ("4K Ultra HD TV 55\"", "Crystal clear 4K display", 799.99, 699.99, "ViewMax", 20),
            ("Laptop Pro 15", "High performance laptop", 1299.99, 1199.99, "CompuTech", 15),
            ("Wireless Earbuds", "True wireless earbuds with charging case", 129.99, 99.99, "AudioTech", 100),
            ("Tablet 10 inch", "Portable tablet for work and play", 449.99, 399.99, "TechTab", 40),
            ("Gaming Console X", "Next-gen gaming console", 499.99, None, "GameZone", 25),
            ("Bluetooth Speaker", "Portable waterproof speaker", 79.99, 59.99, "SoundWave", 80),
            ("Digital Camera", "Professional DSLR camera", 899.99, 799.99, "PhotoPro", 12),
            ("Smart Home Hub", "Control your smart home devices", 149.99, 129.99, "HomeSmart", 45),
        ]
        
        for i, (name, desc, price, disc, brand, stock) in enumerate(electronics):
            products_data.append({
                "name": name, "slug": name.lower().replace(" ", "-").replace("\"", ""),
                "description": desc, "price": price, "discount_price": disc,
                "brand": brand, "sku": f"ELEC-{i+1:04d}", "stock": stock,
                "category_id": categories[0].id, "is_featured": i < 3,
                "images": [f"https://picsum.photos/seed/{i+100}/500/500"]
            })
        
        # Fashion
        fashion = [
            ("Men's Casual T-Shirt", "100% cotton comfortable t-shirt", 29.99, None, "StyleHub", 100),
            ("Women's Summer Dress", "Elegant summer dress", 59.99, 49.99, "Fashionista", 60),
            ("Denim Jeans Classic", "Classic fit denim jeans", 69.99, 59.99, "DenimCo", 80),
            ("Leather Jacket", "Premium leather jacket", 199.99, 179.99, "LeatherCraft", 25),
            ("Running Shoes", "Lightweight running shoes", 89.99, 79.99, "SportStep", 70),
            ("Formal Shirt", "Business formal shirt", 49.99, 39.99, "OfficePro", 90),
            ("Winter Coat", "Warm winter coat", 149.99, 129.99, "WinterWear", 35),
            ("Sneakers Urban", "Trendy urban sneakers", 99.99, 89.99, "StreetStyle", 55),
        ]
        
        for i, (name, desc, price, disc, brand, stock) in enumerate(fashion):
            products_data.append({
                "name": name, "slug": name.lower().replace(" ", "-").replace("'", ""),
                "description": desc, "price": price, "discount_price": disc,
                "brand": brand, "sku": f"FASH-{i+1:04d}", "stock": stock,
                "category_id": categories[1].id, "is_featured": i < 2,
                "images": [f"https://picsum.photos/seed/{i+200}/500/500"]
            })
        
        # Home & Kitchen
        home = [
            ("Coffee Maker Deluxe", "Programmable coffee maker", 89.99, 69.99, "BrewMaster", 40),
            ("Air Fryer Pro", "Healthy cooking air fryer", 129.99, 99.99, "KitchenPro", 35),
            ("Vacuum Cleaner Robot", "Smart robot vacuum", 349.99, 299.99, "CleanBot", 20),
            ("Blender Power", "High-speed blender", 79.99, 69.99, "BlendMax", 50),
            ("Microwave Oven", "Compact microwave oven", 149.99, 129.99, "CookEasy", 30),
            ("Toaster 4-Slice", "Stainless steel toaster", 49.99, 39.99, "ToastPro", 60),
            ("Electric Kettle", "Fast boiling electric kettle", 39.99, 29.99, "HotWater", 80),
            ("Food Processor", "Multi-function food processor", 99.99, 89.99, "ChopMaster", 25),
        ]
        
        for i, (name, desc, price, disc, brand, stock) in enumerate(home):
            products_data.append({
                "name": name, "slug": name.lower().replace(" ", "-"),
                "description": desc, "price": price, "discount_price": disc,
                "brand": brand, "sku": f"HOME-{i+1:04d}", "stock": stock,
                "category_id": categories[2].id, "is_featured": i < 2,
                "images": [f"https://picsum.photos/seed/{i+300}/500/500"]
            })
        
        # Books
        books = [
            ("The Great Novel", "Bestselling fiction novel", 19.99, None, "BookPress", 100),
            ("Learn Python Programming", "Complete Python guide", 39.99, 34.99, "TechBooks", 50),
            ("History of the World", "Comprehensive history book", 29.99, 24.99, "HistoryPress", 40),
            ("Cooking Masterclass", "Professional cooking recipes", 34.99, 29.99, "ChefBooks", 60),
            ("Business Strategy", "Modern business strategies", 24.99, 19.99, "BizBooks", 45),
            ("Science Encyclopedia", "Complete science reference", 49.99, 44.99, "SciencePress", 30),
        ]
        
        for i, (name, desc, price, disc, brand, stock) in enumerate(books):
            products_data.append({
                "name": name, "slug": name.lower().replace(" ", "-"),
                "description": desc, "price": price, "discount_price": disc,
                "brand": brand, "sku": f"BOOK-{i+1:04d}", "stock": stock,
                "category_id": categories[3].id, "is_featured": i < 1,
                "images": [f"https://picsum.photos/seed/{i+400}/500/500"]
            })
        
        # Sports
        sports = [
            ("Yoga Mat Premium", "Non-slip eco-friendly yoga mat", 39.99, 29.99, "FitLife", 70),
            ("Dumbbell Set", "Adjustable dumbbell set", 149.99, 129.99, "IronStrong", 25),
            ("Tennis Racket Pro", "Professional tennis racket", 89.99, 79.99, "CourtKing", 30),
            ("Basketball Official", "Official size basketball", 29.99, 24.99, "HoopStar", 50),
            ("Cycling Helmet", "Safety cycling helmet", 59.99, 49.99, "BikeGear", 40),
            ("Fitness Tracker Band", "Activity tracking band", 49.99, 39.99, "FitTrack", 80),
        ]
        
        for i, (name, desc, price, disc, brand, stock) in enumerate(sports):
            products_data.append({
                "name": name, "slug": name.lower().replace(" ", "-"),
                "description": desc, "price": price, "discount_price": disc,
                "brand": brand, "sku": f"SPRT-{i+1:04d}", "stock": stock,
                "category_id": categories[4].id, "is_featured": i < 2,
                "images": [f"https://picsum.photos/seed/{i+500}/500/500"]
            })
        
        # Beauty
        beauty = [
            ("Face Moisturizer", "Hydrating face cream", 34.99, 29.99, "GlowSkin", 60),
            ("Perfume Elegance", "Luxury fragrance", 79.99, 69.99, "ScentLux", 40),
            ("Hair Dryer Pro", "Professional hair dryer", 59.99, 49.99, "HairCare", 35),
            ("Makeup Kit Complete", "Full makeup set", 89.99, 79.99, "BeautyBox", 25),
            ("Skincare Set", "Complete skincare routine", 69.99, 59.99, "SkinGlow", 45),
        ]
        
        for i, (name, desc, price, disc, brand, stock) in enumerate(beauty):
            products_data.append({
                "name": name, "slug": name.lower().replace(" ", "-"),
                "description": desc, "price": price, "discount_price": disc,
                "brand": brand, "sku": f"BEAU-{i+1:04d}", "stock": stock,
                "category_id": categories[5].id, "is_featured": i < 1,
                "images": [f"https://picsum.photos/seed/{i+600}/500/500"]
            })
        
        # Add all products
        for prod_data in products_data:
            product = Product(**prod_data)
            db.add(product)
        
        print(f"Added {len(products_data)} products")
        
        print("Seeding banners...")
        banners_data = [
            {
                "title": "Summer Sale",
                "subtitle": "Up to 50% off on selected items",
                "image": "https://picsum.photos/seed/banner1/1200/500",
                "link": "/products?is_featured=true",
                "position": 1
            },
            {
                "title": "New Arrivals",
                "subtitle": "Check out our latest collection",
                "image": "https://picsum.photos/seed/banner2/1200/500",
                "link": "/products",
                "position": 2
            },
        ]
        
        for banner_data in banners_data:
            banner = Banner(**banner_data)
            db.add(banner)
        
        db.commit()
        print("Database seeded successfully!")
        print(f"Total products: {len(products_data)}")
        print("Admin: admin@shophub.com / admin123")
        print("User: user@shophub.com / user123")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
