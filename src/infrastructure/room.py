from redis.asyncio import Redis


class RoomRepository:
    def __init__(
        self,
        redis_host: str,
        redis_port: int
    ) -> None:
        self.redis_client = Redis(
            host=redis_host,
            port=redis_port
        )

    async def create_room(
        self,
        room_name: str
    ) -> None:
        await self.redis_client.set(
            room_name,
            ""
        )

    async def is_room_exists(
        self,
        room_name: str
    ) -> bool:
        room = await self.redis_client.exists(room_name)
        return bool(room)

    async def update_content(
        self,
        room_name: str,
        content: str
    ) -> None:
        await self.redis_client.set(room_name, content, nx=False)

    async def get_content(
        self,
        room_name: str
    ) -> str | None:
        return await self.redis_client.get(room_name)
