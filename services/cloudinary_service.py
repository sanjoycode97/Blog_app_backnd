import os
from dotenv import load_dotenv
import cloudinary
import cloudinary.uploader

load_dotenv()

# If CLOUDINARY_URL provided, this single line configures everything automatically.
if os.getenv("CLOUDINARY_URL"):
    cloudinary.config(cloudinary_url=os.getenv("CLOUDINARY_URL"))
else:
    cloudinary.config(
        cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
        api_key=os.getenv("CLOUDINARY_API_KEY"),
        api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    )

def upload_image(file_obj, folder: str = "blog_uploads") -> str:
    """
    Uploads a file-like object to Cloudinary and returns a secure URL.
    """
    result = cloudinary.uploader.upload(file_obj, folder=folder)
    return result["secure_url"]
