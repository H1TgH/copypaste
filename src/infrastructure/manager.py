from fastapi import WebSocket


class ConnectionManager:
    def __init__(
        self
    ) -> None:
        self.connections: dict[str, set[WebSocket]] = {}

    def connect(
        self,
        room_name: str,
        websocket: WebSocket
    ) -> None:
        if room_name not in self.connections:
            self.connections[room_name] = set()

        self.connections[room_name].add(websocket)

    def disconnect(
        self,
        room_name: str,
        websocket: WebSocket
    ) -> None:
        self.connections[room_name].discard(websocket)

        if not self.connections[room_name]:
            self.connections.pop(room_name)

    async def broadcast(
        self,
        room_name: str,
        data: dict
    ) -> None:
        if room_name in self.connections:
            for connection in self.connections[room_name]:
                await connection.send_json(data)

    async def unicast(
        self,
        websocket: WebSocket,
        data: dict
    ) -> None:
        await websocket.send_json(data)


connection_manager = ConnectionManager()
