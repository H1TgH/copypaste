from fastapi import Depends

from core.room import RoomService
from infrastructure.room import RoomRepository
from settings import settings
from infrastructure.manager import ConnectionManager, connection_manager


def get_room_repo() -> RoomRepository:
    return RoomRepository(
        redis_host=settings.redis.host,
        redis_port=settings.redis.port
    )


def get_room_service(
    room_repo: RoomRepository = Depends(get_room_repo)
) -> RoomService:
    return RoomService(room_repo)


def get_connection_manager() -> ConnectionManager:
    return connection_manager
