import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from utils.logger import setup_logging, get_logger
from utils.config import (
    DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD,
    DB_MIN_POOL_SIZE, DB_MAX_POOL_SIZE,
)
from database.async_db import AsyncDatabase
from database.managers.bus_manager import BusManager
from database.managers.camera_manager import CameraManager
from database.managers.info_from_camera_manager import InfoFromCameraManager
from apps.api.routers import router as api_router

setup_logging(level=logging.DEBUG, log_to_file=True)
log = get_logger("[API]")

db: AsyncDatabase | None = None
bus_manager: BusManager | None = None
camera_manager: CameraManager | None = None
info_from_camera_manager: InfoFromCameraManager | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global db, bus_manager, camera_manager, info_from_camera_manager

    log.info("Подключаемся к БД...")
    db = AsyncDatabase(
        db_name=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        min_size=DB_MIN_POOL_SIZE,
        max_size=DB_MAX_POOL_SIZE,
    )
    await db.connect()

    app.state.db = db
    app.state.bus_manager = BusManager(db)
    app.state.camera_manager = CameraManager(db)
    app.state.info_from_camera_manager = InfoFromCameraManager(db)

    log.info("БД подключена [✓]")

    yield


app = FastAPI(title="Bus API", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST, PUT, DELETE, OPTIONS
    allow_headers=["*"],  # Authorization, Content-Type и т.п.
)

app.include_router(api_router, prefix="/api")