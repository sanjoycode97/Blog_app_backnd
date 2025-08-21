from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database.database import get_db
from database.models import DbPost
from routers.schemas import PostBase, PostDisplay
from services.cloudinary_service import upload_image

router = APIRouter(prefix="/posts", tags=["post"])

# Create post (JSON body with optional image_url)
@router.post("", response_model=PostDisplay)
def create_post(request: PostBase, db: Session = Depends(get_db)):
    post = DbPost(title=request.title, content=request.content, image_url=request.image_url)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

# List all posts
@router.get("/all", response_model=List[PostDisplay])
def get_posts(db: Session = Depends(get_db)):
    return db.query(DbPost).order_by(DbPost.id.desc()).all()

# Upload image to Cloudinary (returns URL to use in create_post)
@router.post("/image")
def upload_post_image(image: UploadFile = File(...)):
    try:
        url = upload_image(image.file)
        return {"image_url": url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
