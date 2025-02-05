from datetime import date, datetime
from typing import List, Optional

from pydantic import UUID4, BaseModel

from app.models.album import AlbumStatus


class TrackBase(BaseModel):
    title: str
    track_number: int
    duration: Optional[int] = None


class TrackCreate(TrackBase):
    pass


class Track(TrackBase):
    id: UUID4
    album_id: UUID4
    file_path: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class AlbumBase(BaseModel):
    title: str
    artist: str
    release_date: Optional[date] = None
    genre: Optional[str] = None


class AlbumCreate(AlbumBase):
    pass


class AlbumUpdate(AlbumBase):
    status: Optional[AlbumStatus] = None


class Album(AlbumBase):
    id: UUID4
    status: AlbumStatus
    storage_path: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    tracks: List[Track] = []

    class Config:
        from_attributes = True
