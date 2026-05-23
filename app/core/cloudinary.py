import cloudinary
import cloudinary.uploader
from app.core.config import settings

cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET,
    secure=True
)

def upload_file(file_bytes: bytes, filename: str, folder: str = "nti") -> str:
    safe_filename = filename.replace("/", "_").replace(" ", "_")
    result = cloudinary.uploader.upload(
        file_bytes,
        folder=folder,
        resource_type="auto",
        public_id=safe_filename
    )
    return result["secure_url"]