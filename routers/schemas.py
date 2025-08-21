from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: str
    image_url: Optional[str] = None

class PostDisplay(PostBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True