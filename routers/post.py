from fastapi import APIRouter, Depends, File, UploadFile, Form, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from database.database import get_db
from database.models import DbPost
from routers.schemas import PostDisplay
from services.cloudinary_service import upload_image

router = APIRouter(prefix="/posts", tags=["post"])

# -----------------------------
# Create post (supports JSON or form-data with optional image)
# -----------------------------
@router.post("", response_model=PostDisplay)
async def create_post(
    request: Request,
    title: Optional[str] = Form(None),
    content: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    """
    Create a post. Supports:
    1. JSON body: {"title": "...", "content": "...", "image_url": "..."}
    2. Form-data with optional image file
    """
    data = {}

    # Try to parse JSON body first
    try:
        json_data = await request.json()
        data["title"] = json_data.get("title")
        data["content"] = json_data.get("content")
        data["image_url"] = json_data.get("image_url")
    except:
        # If not JSON, use form-data values
        data["title"] = title
        data["content"] = content
        data["image_url"] = None

    # If file is provided in form-data, upload it
    if image:
        try:
            uploaded_url = upload_image(image.file)
            image.file.close()
            data["image_url"] = uploaded_url
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Image upload failed: {str(e)}")

    # Validate required fields
    if not data.get("title") or not data.get("content"):
        raise HTTPException(status_code=400, detail="Title and content are required.")

    # Create post
    post = DbPost(
        title=data["title"],
        content=data["content"],
        image_url=data["image_url"]
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

# -----------------------------
# List all posts
# -----------------------------
@router.get("/all", response_model=List[PostDisplay])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(DbPost).order_by(DbPost.id.desc()).all()
    return posts
