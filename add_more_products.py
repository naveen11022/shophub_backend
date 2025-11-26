from app.core.database import SessionLocal
from app.models.product import Product, Category
import random

def add_more_products():
    db = SessionLocal()
    
    try:
        # Get existing categories
        categories = db.query(Category).all()
        if not categories:
            print("No categories found. Please run seed_data.py first.")
            return
        
        # Product templates by category
        electronics_products = [
            "Laptop", "Smartphone", "Tablet", "Monitor", "Keyboard", "Mouse", "Webcam",
            "Speakers", "Microphone", "USB Cable", "Power Bank", "Charger", "Earbuds",
            "Gaming Console", "Controller", "VR Headset", "Smart TV", "Soundbar",
            "Router", "External Hard Drive", "SSD", "RAM", "Graphics Card", "Processor"
        ]
        
        fashion_products = [
            "T-Shirt", "Jeans", "Dress", "Jacket", "Sweater", "Hoodie", "Shorts",
            "Skirt", "Blazer", "Coat", "Sneakers", "Boots", "Sandals", "Belt",
            "Watch", "Sunglasses", "Hat", "Scarf", "Gloves", "Socks", "Tie",
            "Backpack", "Handbag", "Wallet"
        ]
        
        home_kitchen_products = [
            "Blender", "Toaster", "Microwave", "Air Fryer", "Pressure Cooker",
            "Mixer", "Food Processor", "Kettle", "Rice Cooker", "Slow Cooker",
            "Knife Set", "Cutting Board", "Pan Set", "Pot Set", "Baking Tray",
            "Measuring Cups", "Storage Containers", "Dish Rack", "Trash Can",
            "Vacuum Cleaner", "Iron", "Laundry Basket", "Towel Set", "Bedsheet Set"
        ]
        
        books_products = [
            "Fiction Novel", "Mystery Thriller", "Romance Novel", "Science Fiction",
            "Fantasy Book", "Biography", "Self-Help Book", "Cookbook", "Travel Guide",
            "History Book", "Science Book", "Art Book", "Poetry Collection",
            "Children's Book", "Comic Book", "Graphic Novel", "Dictionary",
            "Encyclopedia", "Textbook", "Magazine Subscription"
        ]
        
        sports_products = [
            "Yoga Mat", "Dumbbells", "Resistance Bands", "Jump Rope", "Exercise Ball",
            "Foam Roller", "Yoga Blocks", "Running Shoes", "Sports Bottle",
            "Gym Bag", "Fitness Tracker", "Heart Rate Monitor", "Protein Shaker",
            "Workout Gloves", "Knee Sleeves", "Ankle Weights", "Pull-up Bar",
            "Ab Roller", "Kettlebell", "Medicine Ball", "Treadmill", "Exercise Bike",
            "Tennis Racket", "Basketball"
        ]
        
        brands = ["ProTech", "StyleHub", "HomeEssentials", "ReadMore", "FitLife",
                 "TechMaster", "FashionPro", "KitchenKing", "BookWorld", "SportsPro",
                 "EliteGear", "ModernStyle", "SmartHome", "PageTurner", "ActiveLife"]
        
        adjectives = ["Premium", "Professional", "Deluxe", "Ultra", "Pro", "Elite",
                     "Advanced", "Smart", "Modern", "Classic", "Portable", "Wireless",
                     "Ergonomic", "Compact", "Durable"]
        
        # Map categories to product lists
        category_products = {
            "Electronics": electronics_products,
            "Fashion": fashion_products,
            "Home & Kitchen": home_kitchen_products,
            "Books": books_products,
            "Sports": sports_products
        }
        
        # Unsplash image categories
        image_categories = {
            "Electronics": "technology",
            "Fashion": "fashion",
            "Home & Kitchen": "home",
            "Books": "book",
            "Sports": "fitness"
        }
        
        products_added = 0
        
        for category in categories:
            product_list = category_products.get(category.name, electronics_products)
            image_cat = image_categories.get(category.name, "product")
            
            # Add 100 products per category (500 total)
            for i in range(100):
                base_product = random.choice(product_list)
                adjective = random.choice(adjectives)
                brand = random.choice(brands)
                
                name = f"{adjective} {base_product}"
                slug = name.lower().replace(" ", "-") + f"-{products_added + 1}"
                
                base_price = random.uniform(19.99, 499.99)
                has_discount = random.choice([True, False])
                discount_price = round(base_price * random.uniform(0.7, 0.9), 2) if has_discount else None
                
                # Use simple, reliable placeholder images
                colors = {
                    "Electronics": "3B82F6",
                    "Fashion": "EC4899", 
                    "Home & Kitchen": "10B981",
                    "Books": "F59E0B",
                    "Sports": "8B5CF6"
                }
                color = colors.get(category.name, "CCCCCC")
                # Use simple text without special characters
                simple_text = base_product.replace(' ', '+')[:20]  # Limit length
                image_url = f"https://via.placeholder.com/500/{color}/FFFFFF?text={simple_text}"
                
                # Generate unique SKU with timestamp
                import time
                unique_id = int(time.time() * 1000) % 100000
                
                product = Product(
                    name=name,
                    slug=slug,
                    description=f"High-quality {base_product.lower()} with excellent features and performance. Perfect for everyday use.",
                    price=round(base_price, 2),
                    discount_price=discount_price,
                    brand=brand,
                    sku=f"{brand[:3].upper()}-{base_product[:3].upper()}-{unique_id}",
                    stock=random.randint(10, 100),
                    category_id=category.id,
                    is_featured=random.choice([True, False]) if i < 3 else False,
                    images=[image_url]
                )
                
                db.add(product)
                products_added += 1
                
                if products_added % 50 == 0:
                    print(f"Added {products_added} products...")
        
        db.commit()
        print(f"\n✅ Successfully added {products_added} products!")
        print(f"Total products in database: {db.query(Product).count()}")
        
    except Exception as e:
        print(f"❌ Error adding products: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    print("Adding 500 products to the database...")
    add_more_products()
