"""Seed 1000 products to PostgreSQL database"""
from app.core.database import SessionLocal, engine, Base
from app.core.security import get_password_hash
from app.models.user import User
from app.models.product import Product, Category
from app.models.banner import Banner
from app.models.cart import Cart
from app.models.order import Order, OrderItem
from app.models.review import Review
from app.models.wishlist import Wishlist
import random

def seed_database():
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created!")
    
    db = SessionLocal()
    
    try:
        # Check if data exists
        existing = db.query(User).count()
        if existing > 0:
            print(f"Database has {existing} users. Adding more products...")
            existing_products = db.query(Product).count()
            if existing_products >= 1000:
                print(f"Already have {existing_products} products. Skipping.")
                return
        else:
            # Create users first
            print("Creating users...")
            admin = User(email="admin@shophub.com", username="admin", full_name="Admin User",
                        hashed_password=get_password_hash("admin123"), role="admin")
            user = User(email="user@shophub.com", username="johndoe", full_name="John Doe",
                       phone="+1234567890", hashed_password=get_password_hash("user123"), role="customer")
            db.add(admin)
            db.add(user)
            db.flush()
            cart = Cart(user_id=user.id)
            db.add(cart)
        
        # Create/get categories
        categories_data = [
            ("Electronics", "electronics", "Electronic devices and gadgets"),
            ("Fashion", "fashion", "Clothing and accessories"),
            ("Home & Kitchen", "home-kitchen", "Home appliances and kitchenware"),
            ("Books", "books", "Books and literature"),
            ("Sports", "sports", "Sports equipment and gear"),
            ("Beauty", "beauty", "Beauty and personal care"),
            ("Toys & Games", "toys-games", "Toys and games for all ages"),
            ("Automotive", "automotive", "Car parts and accessories"),
            ("Garden", "garden", "Garden tools and plants"),
            ("Health", "health", "Health and wellness products"),
        ]
        
        categories = []
        for name, slug, desc in categories_data:
            cat = db.query(Category).filter(Category.slug == slug).first()
            if not cat:
                cat = Category(name=name, slug=slug, description=desc)
                db.add(cat)
                db.flush()
            categories.append(cat)
        
        print(f"Categories ready: {len(categories)}")
        
        # Product templates per category
        templates = {
            0: [  # Electronics
                ("Wireless Headphones", "Premium audio headphones", "AudioTech", 50, 200),
                ("Smart Watch", "Fitness tracking smartwatch", "TechWear", 100, 400),
                ("Bluetooth Speaker", "Portable wireless speaker", "SoundWave", 30, 150),
                ("Laptop", "High performance laptop", "CompuTech", 500, 2000),
                ("Tablet", "Portable tablet device", "TechTab", 200, 800),
                ("Camera", "Digital camera", "PhotoPro", 300, 1500),
                ("Gaming Console", "Video game console", "GameZone", 300, 600),
                ("Earbuds", "True wireless earbuds", "AudioTech", 50, 250),
                ("Monitor", "Computer monitor", "ViewMax", 150, 800),
                ("Keyboard", "Mechanical keyboard", "TypePro", 50, 200),
            ],
            1: [  # Fashion
                ("T-Shirt", "Cotton casual t-shirt", "StyleHub", 15, 50),
                ("Jeans", "Denim jeans", "DenimCo", 40, 120),
                ("Dress", "Elegant dress", "Fashionista", 50, 200),
                ("Jacket", "Stylish jacket", "UrbanWear", 80, 300),
                ("Sneakers", "Casual sneakers", "FootStyle", 60, 180),
                ("Shirt", "Formal shirt", "OfficePro", 30, 100),
                ("Sweater", "Warm sweater", "CozyWear", 40, 120),
                ("Shorts", "Summer shorts", "CasualFit", 20, 60),
            ],
            2: [  # Home & Kitchen
                ("Coffee Maker", "Automatic coffee machine", "BrewMaster", 50, 200),
                ("Blender", "High-speed blender", "BlendMax", 40, 150),
                ("Air Fryer", "Healthy cooking air fryer", "KitchenPro", 80, 250),
                ("Vacuum Cleaner", "Powerful vacuum", "CleanPro", 100, 400),
                ("Toaster", "Multi-slice toaster", "ToastPro", 25, 80),
                ("Microwave", "Compact microwave", "CookEasy", 80, 250),
                ("Kettle", "Electric kettle", "HotWater", 20, 60),
            ],
            3: [  # Books
                ("Novel", "Bestselling fiction", "BookPress", 10, 30),
                ("Textbook", "Educational textbook", "EduBooks", 30, 100),
                ("Cookbook", "Recipe collection", "ChefBooks", 20, 50),
                ("Biography", "Life story", "BioPress", 15, 40),
                ("Self-Help", "Personal development", "GrowthBooks", 15, 35),
            ],
            4: [  # Sports
                ("Yoga Mat", "Exercise yoga mat", "FitLife", 20, 60),
                ("Dumbbell", "Weight training", "IronStrong", 30, 150),
                ("Tennis Racket", "Professional racket", "CourtKing", 50, 200),
                ("Basketball", "Official basketball", "HoopStar", 20, 50),
                ("Bicycle", "Mountain bike", "BikeGear", 200, 1000),
                ("Fitness Band", "Activity tracker", "FitTrack", 30, 100),
            ],
            5: [  # Beauty
                ("Moisturizer", "Face cream", "GlowSkin", 20, 80),
                ("Perfume", "Luxury fragrance", "ScentLux", 50, 200),
                ("Hair Dryer", "Professional dryer", "HairCare", 40, 150),
                ("Makeup Set", "Complete makeup kit", "BeautyBox", 50, 200),
                ("Skincare Set", "Skincare routine", "SkinGlow", 40, 150),
            ],
            6: [  # Toys
                ("Action Figure", "Collectible figure", "ToyWorld", 15, 50),
                ("Board Game", "Family board game", "GameFun", 20, 60),
                ("Puzzle", "Jigsaw puzzle", "PuzzlePro", 10, 30),
                ("Remote Car", "RC car toy", "SpeedToys", 30, 100),
                ("Building Blocks", "Construction set", "BuildFun", 25, 80),
            ],
            7: [  # Automotive
                ("Car Cover", "Protective cover", "AutoShield", 30, 100),
                ("Floor Mats", "Car floor mats", "CarInterior", 25, 80),
                ("Phone Mount", "Car phone holder", "DriveGear", 15, 40),
                ("Dash Cam", "Dashboard camera", "RoadWatch", 50, 200),
                ("Car Charger", "USB car charger", "PowerDrive", 10, 30),
            ],
            8: [  # Garden
                ("Garden Tools Set", "Complete tool set", "GardenPro", 40, 150),
                ("Plant Pot", "Decorative pot", "PlantHome", 10, 40),
                ("Lawn Mower", "Electric mower", "GreenCut", 150, 500),
                ("Garden Hose", "Flexible hose", "WaterFlow", 20, 60),
                ("Seeds Pack", "Vegetable seeds", "GrowGreen", 5, 20),
            ],
            9: [  # Health
                ("Vitamins", "Daily vitamins", "HealthPlus", 15, 50),
                ("First Aid Kit", "Emergency kit", "SafetyFirst", 20, 60),
                ("Blood Pressure Monitor", "Digital monitor", "HealthTrack", 40, 120),
                ("Massage Gun", "Muscle massager", "RelaxPro", 80, 250),
                ("Water Bottle", "Insulated bottle", "HydroLife", 15, 40),
            ],
        }
        
        adjectives = ["Premium", "Pro", "Elite", "Ultra", "Classic", "Modern", "Deluxe", "Essential", "Advanced", "Smart"]
        colors = ["Black", "White", "Blue", "Red", "Green", "Silver", "Gold", "Gray", "Navy", "Brown"]
        
        print("Generating 1000 products...")
        products_added = 0
        existing_slugs = set(p.slug for p in db.query(Product.slug).all())
        
        for i in range(1000):
            cat_idx = i % len(categories)
            cat = categories[cat_idx]
            cat_templates = templates.get(cat_idx, templates[0])
            template = cat_templates[i % len(cat_templates)]
            
            name_base, desc_base, brand, min_price, max_price = template
            adj = adjectives[i % len(adjectives)]
            color = colors[(i // 10) % len(colors)]
            
            name = f"{adj} {name_base} {color} #{i+1}"
            slug = f"{name_base.lower().replace(' ', '-')}-{color.lower()}-{i+1}"
            
            if slug in existing_slugs:
                continue
            existing_slugs.add(slug)
            
            price = round(random.uniform(min_price, max_price), 2)
            discount = round(price * random.uniform(0.7, 0.95), 2) if random.random() > 0.4 else None
            
            product = Product(
                name=name,
                slug=slug,
                description=f"{desc_base}. High quality {adj.lower()} {name_base.lower()} in {color.lower()}.",
                price=price,
                discount_price=discount,
                brand=brand,
                sku=f"SKU-{cat_idx}-{i+1:05d}",
                stock=random.randint(5, 200),
                category_id=cat.id,
                is_featured=random.random() > 0.9,
                is_active=True,
                images=[f"https://picsum.photos/seed/prod{i+1}/500/500"],
                rating=round(random.uniform(3.5, 5.0), 1),
                review_count=random.randint(0, 100)
            )
            db.add(product)
            products_added += 1
            
            if products_added % 100 == 0:
                print(f"Added {products_added} products...")
                db.flush()
        
        # Add banners
        existing_banners = db.query(Banner).count()
        if existing_banners == 0:
            banners = [
                Banner(title="Summer Sale", subtitle="Up to 50% off", image="https://picsum.photos/seed/banner1/1200/500", link="/products", position=1),
                Banner(title="New Arrivals", subtitle="Check latest products", image="https://picsum.photos/seed/banner2/1200/500", link="/products", position=2),
            ]
            for b in banners:
                db.add(b)
        
        db.commit()
        total = db.query(Product).count()
        print(f"\nDatabase seeded successfully!")
        print(f"Total products: {total}")
        print("Admin: admin@shophub.com / admin123")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
