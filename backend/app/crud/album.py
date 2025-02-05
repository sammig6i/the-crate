from typing import List, Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import select

from app.models.album import Album, AlbumStatus, Track
from app.schemas.album import AlbumCreate, AlbumUpdate, TrackCreate


async def create_album(db: AsyncSession, *, obj_in: AlbumCreate) -> Album:
    """Create a new album."""
    db_obj = Album(
        title=obj_in.title,
        artist=obj_in.artist,
        release_date=obj_in.release_date,
        genre=obj_in.genre,
        status=AlbumStatus.pending,
    )
    db.add(db_obj)
    await db.flush()
    await db.refresh(db_obj)
    return db_obj


async def add_track(
    db: AsyncSession, *, album_id: UUID, track_in: TrackCreate
) -> Track:
    """Add a track to an album."""
    db_obj = Track(
        album_id=album_id,
        title=track_in.title,
        track_number=track_in.track_number,
        duration=track_in.duration,
    )
    db.add(db_obj)
    await db.flush()
    await db.refresh(db_obj)
    return db_obj


async def update_status(db: AsyncSession, *, album_id: UUID, status: str) -> Album:
    """Update album status."""
    query = select(Album).filter(Album.id == album_id)
    result = await db.execute(query)
    album = result.scalar_one_or_none()

    if not album:
        raise ValueError("Album not found")

    album.status = status
    db.add(album)
    await db.flush()
    await db.refresh(album)
    return album


async def get_album(db: AsyncSession, *, album_id: UUID) -> Optional[Album]:
    """Get an album by ID."""
    query = (
        select(Album).options(selectinload(Album.tracks)).filter(Album.id == album_id)
    )
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def get_multi_albums(
    db: AsyncSession,
    *,
    skip: int = 0,
    limit: int = 100,
    genre: Optional[str] = None,
    status: Optional[str] = None,
) -> List[Album]:
    """Get multiple albums with optional filtering."""
    query = select(Album).options(selectinload(Album.tracks))

    if genre:
        query = query.filter(Album.genre == genre)
    if status:
        query = query.filter(Album.status == status)

    result = await db.execute(query.offset(skip).limit(limit))
    return result.scalars().all()


async def get_tracks(db: AsyncSession, *, album_id: UUID) -> List[Track]:
    """Get all tracks for an album."""
    query = (
        select(Track).filter(Track.album_id == album_id).order_by(Track.track_number)
    )
    result = await db.execute(query)
    return result.scalars().all()


async def update_album(
    db: AsyncSession, *, db_obj: Album, obj_in: AlbumUpdate
) -> Album:
    """Update an album."""
    update_data = obj_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_obj, field, value)

    db.add(db_obj)
    await db.flush()
    await db.refresh(db_obj)
    return db_obj


async def remove_album(db: AsyncSession, *, album_id: UUID) -> bool:
    """Delete an album."""
    query = select(Album).filter(Album.id == album_id)
    result = await db.execute(query)
    obj = result.scalar_one_or_none()
    if not obj:
        return False

    await db.delete(obj)
    await db.flush()
    return True


album = {
    "create_album": create_album,
    "add_track": add_track,
    "update_status": update_status,
    "get_album": get_album,
    "get_multi_albums": get_multi_albums,
    "get_tracks": get_tracks,
    "update_album": update_album,
    "remove_album": remove_album,
}
