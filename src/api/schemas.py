from pydantic import BaseModel


class RoomCreationSchema(BaseModel):
    room_name: str


class ContentSchema(BaseModel):
    content: str


class UpdatedContentSchema(BaseModel):
    event_type: str
    new_content: str
