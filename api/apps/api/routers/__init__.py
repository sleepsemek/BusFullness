from fastapi import APIRouter
from .buses import router as buses_router
from .cameras import router as cameras_router
from .measurements import router as measurements_router
from .snapshots import router as snapshots_router
from .routes_avg import router as routes_avg_router

router = APIRouter()
router.include_router(buses_router)
router.include_router(cameras_router)
router.include_router(measurements_router)
router.include_router(snapshots_router)
router.include_router(routes_avg_router)
