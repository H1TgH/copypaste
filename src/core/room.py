from core.exceptions import RoomAlreadyExistsException
from infrastructure.room import RoomRepository


class RoomService:
    def __init__(
        self,
        room_repository: RoomRepository
    ) -> None:
        self.room_repo = room_repository

    async def create_room(
        self,
        room_name: str
    ) -> None:
        await self._check_room_existence(room_name)

        await self.room_repo.create_room(room_name)

    async def is_exists(
        self,
        room_name: str
    ) -> bool:
        return await self.room_repo.is_room_exists(room_name)

    async def _check_room_existence(
        self,
        room_name: str
    ) -> None:
        room_existence = await self.room_repo.is_room_exists(room_name)
        if room_existence:
            raise RoomAlreadyExistsException("Room already exitst")

    async def update_content(
        self,
        room_name: str,
        content: str
    ) -> None:
        await self.room_repo.update_content(room_name, content)

    async def get_content(
        self,
        room_name: str
    ) -> str:
        return await self.room_repo.get_content(room_name)
