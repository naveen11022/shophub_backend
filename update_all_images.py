from app.core.database import SessionLocal
from app.models.product import Product

def update_all_images():
    db = SessionLocal()
    
    try:
        products = db.query(Product).all()
        updated = 0
        
        # Use picsum.photos - very reliable random image service
        for i, product in enumerate(products):
            # Use picsum with seed for consistent images per product
            product.images = [f"https://picsum.photos/seed/{product.id}/500/500"]
            updated += 1
            
            if updated % 100 == 0:
                print(f"Updated {updated} products...")
                db.commit()
        
        db.commit()
        print(f"\n✅ Successfully updated {updated} product images!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("Updating all product images to use reliable placeholders...")
    update_all_images()
