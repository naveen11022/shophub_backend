from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from typing import List
import os
import uuid
from pathlib import Path
from app.api.deps import get_current_admin

router = APIRouter()

# Create uploads directory if it doesn't exist
UPLOAD_DIR = Path("uploads/products")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB


def validate_image(file: UploadFile) -> bool:
    """Validate image file"""
    # Check file extension
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        return False
    
    # Check content type
    if not file.content_type or not file.content_type.startswith("image/"):
        return False
    
    return True


@router.post("/upload/image")
async def upload_image(
    file: UploadFile = File(...),
    current_user = Depends(get_current_admin)
):
    """Upload a single image"""
    
    # Validate file
    if not validate_image(file):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # Read file content
    content = await file.read()
    
    # Check file size
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size: {MAX_FILE_SIZE / (1024*1024)}MB"
        )
    
    # Generate unique filename
    file_ext = os.path.splitext(file.filename)[1].lower()
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = UPLOAD_DIR / unique_filename
    
    # Save file
    try:
        with open(file_path, "wb") as f:
            f.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")
    
    # Return URL
    image_url = f"/uploads/products/{unique_filename}"
    
    return {
        "url": image_url,
        "filename": unique_filename
    }


@router.post("/upload/images")
async def upload_multiple_images(
    files: List[UploadFile] = File(...),
    current_user = Depends(get_current_admin)
):
    """Upload multiple images"""
    
    if len(files) > 10:
        raise HTTPException(status_code=400, detail="Maximum 10 images allowed")
    
    uploaded_images = []
    
    for file in files:
        # Validate file
        if not validate_image(file):
            continue
        
        # Read file content
        content = await file.read()
        
        # Check file size
        if len(content) > MAX_FILE_SIZE:
            continue
        
        # Generate unique filename
        file_ext = os.path.splitext(file.filename)[1].lower()
        unique_filename = f"{uuid.uuid4()}{file_ext}"
        file_path = UPLOAD_DIR / unique_filename
        
        # Save file
        try:
            with open(file_path, "wb") as f:
                f.write(content)
            
            image_url = f"/uploads/products/{unique_filename}"
            uploaded_images.append({
                "url": image_url,
                "filename": unique_filename,
                "original_name": file.filename
            })
        except Exception:
            continue
    
    if not uploaded_images:
        raise HTTPException(status_code=400, detail="No valid images uploaded")
    
    return {
        "images": uploaded_images,
        "count": len(uploaded_images)
    }


@router.delete("/upload/image")
async def delete_image(
    filename: str,
    current_user = Depends(get_current_admin)
):
    """Delete an uploaded image"""
    
    # Security check - ensure filename doesn't contain path traversal
    if ".." in filename or "/" in filename or "\\" in filename:
        raise HTTPException(status_code=400, detail="Invalid filename")
    
    file_path = UPLOAD_DIR / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Image not found")
    
    try:
        os.remove(file_path)
        return {"message": "Image deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete image: {str(e)}")
