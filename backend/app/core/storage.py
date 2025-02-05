import os
import uuid

from app.core.config import settings
from fastapi import UploadFile
from supabase import Client, create_client

supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)


async def upload_file(file: UploadFile) -> str:
    """
    Upload a file to Supabase Storage and return the public URL.
    """
    try:
        # Read file content
        content = await file.read()

        # Generate a unique filename
        file_ext = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_ext}"

        # Upload to Supabase storage
        # The 'music' bucket must be created in Supabase
        response = supabase.storage.from_("music").upload(unique_filename, content)

        # Get public URL
        file_path = supabase.storage.from_("music").get_public_url(unique_filename)

        return file_path

    except Exception as e:
        # Log the error
        print(f"Error uploading file: {str(e)}")
        raise e
    finally:
        await file.seek(0)  # Reset file pointer


async def delete_file(file_path: str) -> bool:
    """
    Delete a file from Supabase Storage.
    """
    try:
        # Extract filename from path
        filename = file_path.split("/")[-1]

        # Delete from Supabase storage
        supabase.storage.from_("music").remove([filename])
        return True

    except Exception as e:
        # Log the error
        print(f"Error deleting file: {str(e)}")
        return False
