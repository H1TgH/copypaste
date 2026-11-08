from functools import wraps

from fastapi import HTTPException, status

from core.exceptions import RoomAlreadyExistsException


def handle_room_exceptions(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)

        except RoomAlreadyExistsException as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(exc)
            ) from exc

    return wrapper
