from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, status

from api.decorators import handle_room_exceptions
from api.schemas import RoomCreationSchema, ContentSchema, UpdatedContentSchema
from core.room import RoomService
from api.dependencies import get_connection_manager, get_room_service
from infrastructure.manager import ConnectionManager


room_router = APIRouter(
    prefix="/room",
    tags=["room"]
)


@room_router.post(
    "/",
    status_code=status.HTTP_201_CREATED
)
@handle_room_exceptions
async def create_room(
    data: RoomCreationSchema,
    service: RoomService = Depends(get_room_service)
):
    await service.create_room(data.room_name)


@room_router.get(
    "/existence/{room_name}",
    status_code=status.HTTP_200_OK
)
@handle_room_exceptions
async def create_room(
    room_name: str,
    service: RoomService = Depends(get_room_service)
):
    existence = await service.is_exists(room_name)

    return {
        "existence": existence
    }


@room_router.websocket(
    "/ws/{room_name}"
)
async def room_ws(
    websocket: WebSocket,
    room_name: str,
    service: RoomService = Depends(get_room_service),
    con_manager: ConnectionManager = Depends(get_connection_manager)
):
    await websocket.accept()
    con_manager.connect(room_name, websocket)

    try:
        content = await service.get_content(room_name)
        content = ContentSchema(
            content=content
        ).model_dump(mode="json")
        await con_manager.unicast(websocket, content)

        while True:
            data = await websocket.receive_json()
            event_type = data["event_type"]
            
            if event_type == "update_content":
                new_content = data["new_content"]
                await service.update_content(room_name, new_content)
                await con_manager.broadcast(room_name, data) 

    except WebSocketDisconnect as exc:
        print(f"WS disconnected: code={exc.code}, reason={exc.reason!r}")
    except Exception as exc:
        print(f"WS error: {type(exc).__name__}: {exc}")
        raise

    finally:
        con_manager.disconnect(room_name, websocket)

