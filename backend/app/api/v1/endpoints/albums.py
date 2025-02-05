from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.crud import album as crud_album
from app.schemas.album import Album, Track

router = APIRouter()


@router.get("/", response_model=List[Album])
async def list_albums(
    db: AsyncSession = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    genre: Optional[str] = None,
    status: Optional[str] = None,
):
    """
    Retrieve albums with pagination and optional filtering.
    """
    albums = await crud_album.get_multi_albums(
        db=db, skip=skip, limit=limit, genre=genre, status=status
    )
    return albums


@router.get("/{album_id}", response_model=Album)
async def get_album(
    album_id: UUID,
    db: AsyncSession = Depends(deps.get_db),
):
    """
    Get album by ID.
    """
    album = await crud_album.get_album(db=db, album_id=album_id)
    if not album:
        raise HTTPException(status_code=404, detail="Album not found")
    return album


@router.get("/{album_id}/tracks", response_model=List[Track])
async def get_album_tracks(
    album_id: UUID,
    db: AsyncSession = Depends(deps.get_db),
):
    """
    Get tracks for a specific album.
    """
    tracks = await crud_album.get_tracks(db=db, album_id=album_id)
    if not tracks:
        raise HTTPException(status_code=404, detail="Album not found or has no tracks")
    return tracks


@router.get("/stream/{track_id}")
async def stream_track(
    track_id: UUID,
    db: AsyncSession = Depends(deps.get_db),
):
    """
    TODO Stream a track. This endpoint will be implemented later with proper streaming functionality.
    """
    raise HTTPException(
        status_code=501, detail="Streaming functionality not implemented yet"
    )
