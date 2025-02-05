from datetime import date

from app.crud.album import album
from app.db.session import AsyncSessionLocal
from app.models.album import AlbumStatus
from app.schemas.album import AlbumCreate, TrackCreate

sample_albums = [
    {
        "title": "Dark Side of the Moon",
        "artist": "Pink Floyd",
        "release_date": date(1973, 3, 1),
        "genre": "Progressive Rock",
        "tracks": [
            {"title": "Speak to Me", "track_number": 1, "duration": 90},
            {"title": "Breathe", "track_number": 2, "duration": 163},
            {"title": "On the Run", "track_number": 3, "duration": 216},
        ],
    },
    {
        "title": "Kind of Blue",
        "artist": "Miles Davis",
        "release_date": date(1959, 8, 17),
        "genre": "Jazz",
        "tracks": [
            {"title": "So What", "track_number": 1, "duration": 561},
            {"title": "Freddie Freeloader", "track_number": 2, "duration": 589},
            {"title": "Blue in Green", "track_number": 3, "duration": 327},
        ],
    },
]


async def seed_data(db) -> None:
    """Seed the database with sample data."""
    for album_data in sample_albums:
        tracks = album_data.pop("tracks")
        album_in = AlbumCreate(**album_data)
        db_album = await album["create"](db, obj_in=album_in)

        # Create tracks for the album
        for track_data in tracks:
            track_in = TrackCreate(**track_data)
            await album["add_track"](db, album_id=db_album.id, track_in=track_in)

        # Set first album as approved, second as pending
        if album_data["title"] == "Dark Side of the Moon":
            await album["update_status"](
                db, album_id=db_album.id, status=AlbumStatus.approved
            )

    await db.commit()


async def main() -> None:
    """Main function to run the seeding process."""
    async with AsyncSessionLocal() as db:
        await seed_data(db)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
