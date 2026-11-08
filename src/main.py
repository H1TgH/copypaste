from pathlib import Path

from fastapi import APIRouter, FastAPI
from fastapi.staticfiles import StaticFiles

from api.room import room_router


app = FastAPI()

api_v1_router = APIRouter(prefix="/api/v1")
api_v1_router.include_router(room_router)

app.include_router(api_v1_router)

app.mount("/", StaticFiles(directory=Path(__file__).parent / "static", html=True), name="static")
