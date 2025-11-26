from app.core.database import SessionLocal
from app.models.product import Product
import json

def fix_images():
    db = SessionLocal()
    
    try:
        products = db.query(Product).all()
        fixed_count = 0
        
        for product in products:
            # Check if images is a string instead of list
            if isinstance(product.images, str):
                try:
                    # Try to parse JSON string
                    product.images = json.loads(product.images)
                    fixed_count += 1
                except:
                    # If parsing fails, create a simple placeholder
                    product.images = ["https://via.placeholder.com/500/CCCCCC/666666?text=Product"]
                    fixed_count += 1
            elif product.images is None or len(product.images) == 0:
                # If no images, add placeholder
                product.images = ["https://via.placeholder.com/500/CCCCCC/666666?text=Product"]
                fixed_count += 1
        
        db.commit()
        print(f"✅ Fixed {fixed_count} products with image issues")
        print(f"Total products: {len(products)}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("Fixing product images...")
    fix_images()
