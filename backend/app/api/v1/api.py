from app.api.v1.endpoints import admin, albums
from fastapi import APIRouter

api_router = APIRouter()

api_router.include_router(albums.router, prefix="/albums", tags=["albums"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
