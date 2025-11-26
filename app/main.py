from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.api.routes import auth, products, cart, orders, reviews, wishlist, banners, admin, upload
from app.core.config import settings

app = FastAPI(
    title="ShopHub API",
    description="Modern Ecommerce Platform API",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create uploads directory
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

# Mount static files
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(products.router, prefix="/api", tags=["Products"])
app.include_router(cart.router, prefix="/api", tags=["Cart"])
app.include_router(orders.router, prefix="/api", tags=["Orders"])
app.include_router(reviews.router, prefix="/api", tags=["Reviews"])
app.include_router(wishlist.router, prefix="/api", tags=["Wishlist"])
app.include_router(banners.router, prefix="/api", tags=["Banners"])
app.include_router(admin.router, prefix="/api", tags=["Admin"])
app.include_router(upload.router, prefix="/api", tags=["Upload"])


@app.get("/")
def root():
    return {"message": "Welcome to ShopHub API"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
