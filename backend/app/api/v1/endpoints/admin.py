import json
from typing import List
from uuid import UUID

from app.api import deps
from app.core.storage import upload_file
from app.crud import album as crud_album
from app.schemas.album import Album, AlbumCreate, AlbumUpdate
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.post("/albums", response_model=Album)
async def create_album(
    *,
    db: AsyncSession = Depends(deps.get_db),
    album_data: str = Form(...),
    audio_files: List[UploadFile] = File(...),
):
    """
    Create a new album with tracks (admin only).
    """
    try:
        album_data_dict = json.loads(album_data)
        album_in = AlbumCreate(**album_data_dict)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid album data format")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Upload files to storage and create album
    storage_paths = []
    try:
        for audio_file in audio_files:
            storage_path = await upload_file(audio_file)
            storage_paths.append(storage_path)

        album = await crud_album.create_album_with_tracks(
            db=db, album_in=album_in, track_files=list(zip(audio_files, storage_paths))
        )
    except Exception as e:
        # TODO: Clean up uploaded files if album creation fails
        raise HTTPException(status_code=500, detail=str(e))

    return album


@router.put("/albums/{album_id}", response_model=Album)
async def update_album(
    *,
    db: AsyncSession = Depends(deps.get_db),
    album_id: UUID,
    album_in: AlbumUpdate,
):
    """
    Update album details (admin only).
    """
    album = await crud_album.get_album(db=db, album_id=album_id)
    if not album:
        raise HTTPException(status_code=404, detail="Album not found")

    album = await crud_album.update_album(db=db, db_obj=album, obj_in=album_in)
    return album


@router.delete("/albums/{album_id}")
async def delete_album(
    *,
    db: AsyncSession = Depends(deps.get_db),
    album_id: UUID,
):
    """
    Delete an album (admin only).
    """
    album = await crud_album.get_album(db=db, album_id=album_id)
    if not album:
        raise HTTPException(status_code=404, detail="Album not found")

    await crud_album.delete_album(db=db, album_id=album_id)
    return {"message": "Album deleted successfully"}


@router.post("/albums/{album_id}/approve")
async def approve_album(
    *,
    db: AsyncSession = Depends(deps.get_db),
    album_id: UUID,
):
    """
    Approve a pending album (admin only).
    """
    album = await crud_album.get_album(db=db, album_id=album_id)
    if not album:
        raise HTTPException(status_code=404, detail="Album not found")

    album = await crud_album.update_album_status(
        db=db, album_id=album_id, status="approved"
    )
    return {"message": "Album approved successfully"}


@router.post("/albums/{album_id}/reject")
async def reject_album(
    *,
    db: AsyncSession = Depends(deps.get_db),
    album_id: UUID,
):
    """
    Reject a pending album (admin only).
    """
    album = await crud_album.get_album(db=db, album_id=album_id)
    if not album:
        raise HTTPException(status_code=404, detail="Album not found")

    album = await crud_album.update_album_status(
        db=db, album_id=album_id, status="rejected"
    )
    return {"message": "Album rejected successfully"}
